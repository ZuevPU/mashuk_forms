# mashuk_forms

Анкета и админка семинара Машук.

Публичная форма: `/`
Админка: `/admin`
АПИ заявок: `POST /apply`
Проверка: `GET /health`

Репозиторий: https://github.com/ZuevPU/mashuk_forms

## Структура

```
app.py              FastAPI
admin_api.py        admin API, Excel
schema.sql          PostgreSQL
static/             form + admin HTML
uploads/            files, not in git
tools/              HTML builders
tilda/              Tilda iframe
consent/            consent source
deploy/             nginx, systemd, Timeweb start
```

## Локальный запуск

1. PostgreSQL
2. Copy `.env.example` to `.env`
3. Run:

```powershell
.\run.ps1
```

Публичная форма: http://127.0.0.1:8000
Админка: http://127.0.0.1:8000/admin

В .env задайте ADMIN_PASSWORD и ADMIN_SECRET. Пароль и DATABASE_URL в git не класть.

## Timeweb + GitHub

1. В Timeweb Apps подключите этот репозиторий (main).
2. Корень приложения — корень репозитория.
3. `pip install -r requirements.txt`
4. Стартовая команда:

```
gunicorn -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 app:app
```

`sh deploy/start.sh`

5. Переменные окружения только в панели Timeweb:

- `DATABASE_URL`
- `ADMIN_PASSWORD`
- `ADMIN_SECRET`
- `UPLOAD_DIR=./uploads`
- `MAX_FILE_MB=20`
- `CORS_ORIGINS`
- `FRAME_ANCESTORS` — `https://*.tilda.ws https://*.tilda.cc`

6. В Тильде, блок HTML (T123), код из `tilda/tilda-iframe-block.html`

Админку в iframe не встраивать.

## Excel и фильтры

В админке таблица заявок, сортировка, фильтры и выгрузка Excel. Клик по строке открывает карточку.
