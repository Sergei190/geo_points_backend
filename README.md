# Backend-приложение на Django для работы с гео-точками

## Описание

Backend-приложение на Django для работы с географическими точками на карте. Предоставляет REST API для создания точек, обмена сообщениями и поиска контента в заданном радиусе от указанных координат.

## Технический стек

*   Python 3.10+
*   Django 4+ / 5+
*   Django REST Framework (DRF)
*   PostgreSQL / PostGIS
*   GeoDjango
*   Django TestCase

## Функционал

*   **Создание точки на карте:** `POST /api/geopoints/`
*   **Создание комментария к заданной точке:** `POST /api/comments/`
*   **Поиск точек в заданном радиусе:** `GET /api/geopoints/search/` (параметры: `latitude`, `longitude`, `radius_km`)
*   **Поиск комментариев в заданном радиусе:** `GET /api/comments/search/` (параметры: `latitude`, `longitude`, `radius_km`)
*   **Безопасность:** Все эндпоинты защищены аутентификацией (`IsAuthenticated`).

## Установка и запуск

1.  **Клонирование репозитория:**
    ```bash
    git clone <URL_ВАШЕГО_РЕПОЗИТОРИЯ>
    cd geo_points_backend
    ```

2.  **Создание и активация виртуального окружения (рекомендуется):**
    ```bash
    # Создание окружения (например, с помощью venv)
    python -m venv venv

    # Активация (Windows)
    venv\Scripts\activate
    # Активация (Linux/Mac)
    source venv/bin/activate
    ```

3.  **Установка зависимостей:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Настройка PostgreSQL:**
    *   Установите PostgreSQL и PostGIS.
    *   Создайте базу данных для разработки (например, `geo_points_dev_db`).
    *   Подключитесь к созданной базе данных.
    *   Выполните команду: `CREATE EXTENSION postgis;`.

5.  **Настройка переменных окружения:**
    *   Создайте файл `.env` в корне проекта.
    *   Укажите настройки подключения к PostgreSQL (пример в `.env.example`):
        ```env
        DEV_DB_NAME=geo_points_dev_db
        DEV_DB_USER=postgres
        DEV_DB_PASSWORD=Ser19052001
        DEV_DB_HOST=localhost
        DEV_DB_PORT=5432

        TEST_DB_NAME=geo_points_test_db
        TEST_DB_USER=postgres
        TEST_DB_PASSWORD=Ser19052001
        TEST_DB_HOST=localhost
        TEST_DB_PORT=5432
        ```

6.  **Применение миграций:**
    ```bash
    python manage.py migrate
    ```

7.  **(Опционально) Создание суперпользователя:**
    ```bash
    python manage.py createsuperuser
    ```

8.  **Запуск сервера разработки:**
    ```bash
    python manage.py runserver
    ```

    Приложение будет доступно по адресу `http://127.0.0.1:8000/`.

## Запуск тестов

Для запуска тестов используется отдельная тестовая база данных PostgreSQL.

1.  Убедитесь, что PostgreSQL запущен и в файле `.env` указаны настройки для тестовой базы данных (например, `TEST_DB_NAME=geo_points_test_db`).
2.  Убедитесь, что расширение `postgis` установлено в тестовой базе данных.
3.  Выполните команду:
    ```bash
    python manage.py test --settings=geo_points_project.settings.test_postgis
    ```