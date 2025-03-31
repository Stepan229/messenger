
## API

### Аутентификация (users/)

*   **Регистрация пользователя:** `POST /api/register/`
*   **Вход пользователя:** `POST /api/login/`
*   **Выход пользователя:** `POST /api/logout/`

### Чаты и Сообщения (messanger/)

*   **Получение списка чатов пользователя:** `GET /api/chats/` 
*   **Создание чата:** `POST /api/chats/create/` 
*   **Получение списка сообщений в чате:** `GET /api/chat/{room_id}/messages/`
*   **Создание сообщения в чате:** `POST /api/chat/{room_id}/messages/create/` 
*   **Изменение сообщения:** `PUT /api/chat/{room_id}/messages/{message_id}/` 
*   **Удаление сообщения:** `DELETE /api/chat/{room_id}/messages/{message_id}/` 

## Live-chat

*   **Страница с Live-chat:** `api/chat/{room_id}`

## Модели

*   **User:**  (users/models.py) 
*   **Chat:** (messanger/models.py) 
*   **UserChat:**  (messanger/models.py) 
*   **Message:** (messanger/models.py) 


## Установка и запуск

1.  **Клонируйте репозиторий:**
    ```bash
    git clone [URL вашего репозитория]
    cd [имя вашего репозитория]
    ```

2.  **Создайте и активируйте виртуальное окружение:**
    ```bash
    python -m venv venv
    # Linux/macOS
    source venv/bin/activate
    # Windows
    .\venv\Scripts\activate
    ```

3.  **Установите зависимости:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Примените миграции базы данных:**
    ```bash
    python manage.py migrate
    ```

5.  **Создайте суперпользователя:**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Запустите сервер разработки:**
    ```bash
    python manage.py runserver
    ```
    *Для работы WebSockets*
    ```bash
    daphne social_network.asgi:application
    ```