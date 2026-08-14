# Vladivostok Transport Project

aka Train project 2

Базовый шаблон сайта на FastAPI с HTML-шаблонами (Jinja2) и статикой.

## Структура

- `app/main.py` — точка входа FastAPI
- `app/routers/pages.py` — маршруты страниц
- `app/templates/` — HTML-шаблоны
- `app/static/` — CSS/JS/изображения

## Быстрый старт

1. Создайте и активируйте виртуальное окружение:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Установите зависимости:

```powershell
pip install -r requirements.txt
```

3. Запустите сервер:

```powershell
uvicorn app.main:app --reload
```

4. Откройте в браузере:

- `http://127.0.0.1:8000`

## Что уже есть

- Маршрут `GET /` с рендерингом `index.html`
- Подключение статики через `/static`
- Готовая базовая верстка (`base.html`) и стили
