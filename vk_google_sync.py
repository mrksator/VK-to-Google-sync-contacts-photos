import vk_api
import requests
import os.path
import re
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ПОЛУЧИТЬ ТОКЕН / GET TOKEN : https://vkhost.github.io/ (Настройки > Друзья)
VK_ACCESS_TOKEN = '' # <-- ВСТАВЬТЕ СВОЙ ТОКЕН ЗДЕСЬ / PUT YOUR TOKEN HERE

SCOPES = ['https://www.googleapis.com/auth/contacts']
GOOGLE_CREDS_FILE = 'credentials.json'
GOOGLE_TOKEN_FILE = 'token.json'


def normalize_phone(phone):
    "Приводит номер телефона к единому формату (только цифры)."
    if not phone:
        return None
    return re.sub(r'\D', '', phone)

def authenticate_google():
    "Аутентификация в Google API и получение сервисного объекта."
    creds = None
    if os.path.exists(GOOGLE_TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(GOOGLE_TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(GOOGLE_TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('people', 'v1', credentials=creds)
        return service
    except HttpError as err:
        print(f"Произошла ошибка при подключении к Google API: {err}")
        return None

def get_vk_friends(vk_session):
    "Получение списка друзей из ВКонтакте с фото и телефонами."
    try:
        friends = vk_session.method('friends.get', {
            'fields': 'photo_max_orig,contacts,mobile_phone'
        })
        print(f"Найдено {friends['count']} друзей в ВК.")
        return friends['items']
    except vk_api.ApiError as error:
        print(f"Ошибка API ВКонтакте: {error}")
        return []

def get_google_contacts(service):
    "Получение всех контактов Google и создание словаря {телефон: контакт}."
    contacts_map = {}
    try:
        results = service.people().connections().list(
            resourceName='people/me',
            pageSize=2000,
            personFields='names,phoneNumbers'
        ).execute()
        connections = results.get('connections', [])
        for person in connections:
            phone_numbers = person.get('phoneNumbers', [])
            for phone_entry in phone_numbers:
                phone_number = phone_entry.get('value')
                normalized_phone = normalize_phone(phone_number)
                if normalized_phone:
                    contacts_map[normalized_phone] = person
        print(f"Загружено {len(contacts_map)} номеров из Google Контактов.")
        return contacts_map
    except HttpError as err:
        print(f"Произошла ошибка при получении контактов Google: {err}")
        return {}

def main():
    "Основная логика скрипта."
    if 'ВАШ_VK_ТОКЕН_СЮДА' in VK_ACCESS_TOKEN:
        print("Ошибка: Пожалуйста, вставьте ваш токен доступа ВКонтакте в переменную VK_ACCESS_TOKEN в файле скрипта.")
        return

    print("1. Авторизация в Google...")
    google_service = authenticate_google()
    if not google_service:
        return

    print("\n2. Авторизация в ВКонтакте...")
    try:
        vk_session = vk_api.VkApi(token=VK_ACCESS_TOKEN)
        print("Авторизация в ВК прошла успешно.")
    except Exception as e:
        print(f"Не удалось авторизоваться в ВК. Проверьте токен. Ошибка: {e}")
        return

    print("\n3. Получение списка друзей из ВК...")
    vk_friends = get_vk_friends(vk_session)
    if not vk_friends:
        print("Не удалось получить список друзей или он пуст.")
        return

    print("\n4. Получение контактов из Google...")
    google_contacts_map = get_google_contacts(google_service)
    if not google_contacts_map:
        print("Не удалось получить контакты Google или список пуст.")
        return

    print("\n5. Сопоставление контактов и обновление фотографий...")
    updated_count = 0
    skipped_count = 0

    for friend in vk_friends:
        friend_name = f"{friend.get('first_name', '')} {friend.get('last_name', '')}"
        vk_phone = friend.get('mobile_phone')
        vk_photo_url = friend.get('photo_max_orig')

        if not vk_phone or not vk_photo_url:
            continue

        normalized_vk_phone = normalize_phone(vk_phone)

        google_contact = google_contacts_map.get(normalized_vk_phone)
        if google_contact:
            contact_name = google_contact.get('names', [{}])[0].get('displayName', 'Имя не найдено')
            print(f"\nНайдено совпадение: ВК '{friend_name}' ({vk_phone}) <-> Google '{contact_name}'")

            try:
                photo_response = requests.get(vk_photo_url)
                photo_response.raise_for_status()
                photo_bytes = photo_response.content

                google_service.people().updateContactPhoto(
                    resourceName=google_contact['resourceName'],
                    body={
                        'photoBytes': base64.b64encode(photo_bytes).decode('utf-8')
                    }
                ).execute()

                print(f"  [SUCCESS] Фото для контакта '{contact_name}' успешно обновлено!")
                updated_count += 1

            except requests.RequestException as e:
                print(f"  [ERROR] Не удалось скачать фото для {friend_name}: {e}")
            except HttpError as e:
                print(f"  [ERROR] Не удалось обновить фото в Google для {contact_name}: {e}")
            except Exception as e:
                print(f"  [ERROR] Произошла неизвестная ошибка при обработке {contact_name}: {e}")
        else:
            skipped_count += 1

    print("\n--- Завершено ---")
    print(f"Обновлено фотографий: {updated_count}")
    print(f"Пропущено друзей (нет совпадения по номеру): {skipped_count}")
    print(f"Друзей без открытого номера в ВК: {len(vk_friends) - updated_count - skipped_count}")


if __name__ == '__main__':
    main()