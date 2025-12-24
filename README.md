# Backend-приложение на Django для работы с гео-точками

## Описание

Это backend-приложение на Django, предоставляющее REST API для работы с географическими точками на карте. Приложение позволяет создавать точки, оставлять сообщения к ним и искать точки и сообщения в заданном радиусе от указанных координат. Всё API защищено аутентификацией.

## Технический стек

- Python 3.10+
- Django 4+
- Django REST Framework (DRF)
- SQLite (для разработки)
- GeoDjango (для работы с географическими данными)

## Установка и запуск

### Локальный запуск (с SQLite)

1.  Убедитесь, что у вас установлены Python 3.10+, `pip`, `virtualenv` (рекомендуется).
2.  Клонируйте репозиторий:
    ```bash
    git clone <URL_ВАШЕГО_РЕПОЗИТОРИЯ>
    cd geo_points_backend
    ```
3.  Создайте и активируйте виртуальное окружение:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    # или
    venv\Scripts\activate  # Windows
    ```
4.  Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```
5.  Установите системные зависимости для GeoDjango (Ubuntu/Debian):
    ```bash
    sudo apt-get install binutils gdal-bin libproj-dev libgeos-dev
    # Для Windows: установка может отличаться, см. документацию GeoDjango.
    ```
6.  Создайте файл `.env` в корне проекта (пример уже в репозитории) и убедитесь, что переменные `DB_NAME` и т.д. не установлены, чтобы использовалась SQLite.
7.  Выполните миграции:
    ```bash
    python manage.py migrate
    ```
8.  Создайте суперпользователя (для доступа к админке и тестирования):
    ```bash
    python manage.py createsuperuser
    ```
9.  Запустите сервер разработки:
    ```bash
    python manage.py runserver
    ```
    Приложение будет доступно по адресу `http://127.0.0.1:8000/`.

### Запуск с Docker

1.  Убедитесь, что у вас установлены Docker и Docker Compose.
2.  Следуйте шагам 1-5 из "Локального запуска", но не нужно устанавливать Python и pip локально.
3.  Убедитесь, что в файле `.env` не установлены переменные `DB_NAME`, `DB_USER` и т.д., чтобы Docker Compose использовал SQLite.
4.  Выполните команду:
    ```bash
    docker-compose up --build
    ```
    Приложение будет доступно по адресу `http://127.0.0.1:8000/`. Для остановки используйте `Ctrl+C`.

## API Endpoints

Все эндпоинты требуют аутентификации через сессию (SessionAuthentication) или токен (если будет добавлено).

### 1. Создание точки

- **URL**: `POST /api/points/`
- **Headers**: `Content-Type: application/json`
- **Auth Required**: Yes
- **Body**:
  ```json
  {
    "name": "Название точки",
    "description": "Описание точки (опционально)",
    "latitude": 55.7558,
    "longitude": 37.6173
  }