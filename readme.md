# VK-to-Google sync contacts photos

Этот Python-скрипт синхронизирует фотографии профилей друзей из ВКонтакте (VK) с соответствующими контактами в Google, используя мобильный телефон в качестве ключа для сопоставления. Требуется токен VK и учетные данные Google API.

# Синхронизация фото контактов: ВКонтакте -> Google Контакты

Этот скрипт на Python автоматически находит ваших друзей из ВКонтакте в списке контактов Google по номеру телефона и обновляет фотографии в их контактных профилях.

## Основные возможности

* **Авторизация**: Безопасная OAuth-аутентификация в Google и авторизация по токену в VK.
* **Получение данных**: Скрипт запрашивает список друзей из ВКонтакте, включая их имена, фото и номера мобильных телефонов.
* **Сопоставление**: Находит совпадения между друзьями VK и контактами Google по нормализованному номеру телефона (очищенному от лишних символов).
* **Обновление фото**: Если совпадение найдено, скрипт скачивает фотографию в максимальном качестве из профиля VK и загружает ее в соответствующий контакт Google.
* **Подробный лог**: В процессе работы скрипт выводит в консоль информацию о найденных совпадениях, успешных обновлениях и возникших ошибках.

## Подготовка к работе

Перед запуском скрипта необходимо выполнить несколько шагов для настройки доступа к API. 

### Шаг 1: Настройка API Google

1.  **Создайте проект в Google Cloud**:
    * Перейдите в [Google Cloud Console](https://console.cloud.google.com/).
    * Создайте новый проект или выберите существующий.

2.  **Включите People API**:
    * В меню навигации выберите "APIs & Services" -> "Library" (API и сервисы -> Библиотека).
    * Найдите и включите **People API**.

3.  **Настройте OAuth 2.0**:
    * Перейдите в "APIs & Services" -> "OAuth consent screen" (Окно запрашиваемого доступа OAuth).
    * Выберите тип пользователя **External** (Внешний) и нажмите "Create".
    * Заполните обязательные поля (название приложения, email) и сохраните. На этапе "Test users" добавьте свой Google-аккаунт.
    * Перейдите во вкладку **Credentials** (Учетные данные).
    * Нажмите **Create Credentials** -> **OAuth client ID**.
    * Выберите тип приложения **Desktop app** (Компьютерное приложение).
    * Нажмите **Create**. Появится окно с вашими `Client ID` и `Client Secret`. Нажмите **DOWNLOAD JSON**.

4.  **Добавьте файл в проект**:
    * Переименуйте скачанный файл в `credentials.json`.
    * Поместите этот файл в ту же папку, где находится ваш скрипт `vk_google_sync.py`.

> **ВАЖНО**: Файл `credentials.json` содержит секретные ключи. **Никогда** не публикуйте его и добавьте в `.gitignore`.

### Шаг 2: Получение токена ВКонтакте

1.  Перейдите на сервис [VK Host](https://vkhost.github.io/).
2.  Выберите опцию "Только HTTPS", чтобы обезопасить соединение.
3.  Нажмите кнопку "Получить токен", в настройках приложения выберите **"Друзья"**.
4.  Войдите в свой аккаунт и разрешите доступ.
5.  Скопируйте полученный токен из адресной строки (длинная строка символов после `access_token=`).
6.  Откройте файл `vk_google_sync.py` и вставьте скопированный токен в переменную `VK_ACCESS_TOKEN`.

```python
VK_ACCESS_TOKEN = 'СЮДА_ВСТАВИТЬ_СКОПИРОВАННЫЙ_ТОКЕН'
```
> **ПРЕДУПРЕЖДЕНИЕ**: Не сохраняйте файл с вашим реальным токеном в системе контроля версий (Git). Перед коммитом всегда очищайте это поле.

## Установка и запуск

1.  **Клонируйте репозиторий**:
    ```bash
    git clone [https://github.com/mrksator/VK-to-Google-sync-contacts-photos.git](https://github.com/YOUR_LOGIN
    VK-to-Google-sync-contacts-photos.git)
    cd VK-to-Google-sync-contacts-photos
    ```

2.  **Установите зависимости**:
    Рекомендуется использовать виртуальное окружение.
    ```bash
    # Создание и активация виртуального окружения (опционально)
    python -m venv venv
    source venv/bin/activate  # Для Windows: venv\Scripts\activate

    # Установка библиотек
    pip install -r requirements.txt
    ```

3.  **Запустите скрипт**:
    ```bash
    python vk_google_sync.py
    ```

При первом запуске скрипт попросит вас пройти аутентификацию в Google: в браузере откроется страница, где нужно будет выбрать свой аккаунт и разрешить доступ приложению. После этого будет создан файл `token.json` для последующих запусков.

# Contact Photo Synchronization: VKontakte -> Google Contacts

This Python script automatically finds your VKontakte friends in your Google Contacts list using their phone number and updates the photos in their contact profiles.

## Key Features

* **Authorization**: Secure OAuth authentication for Google and token-based authorization for VK.
* **Data Retrieval**: The script requests a list of friends from VKontakte, including their names, photos, and mobile phone numbers.
* **Matching**: Finds matches between VK friends and Google contacts using a normalized phone number (cleaned of extra characters).
* **Photo Update**: If a match is found, the script downloads the photo in maximum quality from the VK profile and uploads it to the corresponding Google contact.
* **Detailed Log**: During execution, the script outputs information to the console about found matches, successful updates, and encountered errors.

## Pre-Requisites

Before running the script, you need to complete a few steps to set up API access.

### Step 1: Google API Setup

1.  **Create a Project in Google Cloud**:
    * Go to the [Google Cloud Console](https://console.cloud.google.com/).
    * Create a new project or select an existing one.

2.  **Enable the People API**:
    * In the navigation menu, select "APIs & Services" -> "Library".
    * Search for and enable the **People API**.

3.  **Configure OAuth 2.0**:
    * Go to "APIs & Services" -> "OAuth consent screen".
    * Select the user type **External** and click "Create".
    * Fill in the required fields (application name, email) and save. In the "Test users" step, add your Google account.
    * Go to the **Credentials** tab.
    * Click **Create Credentials** -> **OAuth client ID**.
    * Select the application type **Desktop app**.
    * Click **Create**. A window with your `Client ID` and `Client Secret` will appear. Click **DOWNLOAD JSON**.

4.  **Add the File to the Project**:
    * Rename the downloaded file to `credentials.json`.
    * Place this file in the same folder as your `vk_google_sync.py` script.

> **IMPORTANT**: The `credentials.json` file contains secret keys. **Never** publish it and add it to `.gitignore`.

##

## Installation and Running

1.  **Clone the Repository**:
    ```bash
    git clone [https://github.com/mrksator/VK-to-Google-sync-contacts-photos.git](https://github.com/YOUR_LOGIN
    VK-to-Google-sync-contacts-photos.git)
    cd VK-to-Google-sync-contacts-photos
    ```

2.  **Install Dependencies**:
    It is recommended to use a virtual environment.
    ```bash
    # Creating and activating a virtual environment (optional)
    python -m venv venv
    source venv/bin/activate  # For Windows: venv\Scripts\activate

    # Installing libraries
    pip install -r requirements.txt
    ```

3.  **Run the Script**:
    ```bash
    python vk_google_sync.py
    ```

On the first run, the script will prompt you to authenticate with Google: a page will open in your browser where you will need to select your account and grant access to the application. After this, a `token.json` file will be created for subsequent runs.
