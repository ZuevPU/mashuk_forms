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

1. Backend → FastAPI, репо `ZuevPU/mashuk_forms`, ветка `main`.
2. **Путь до директории проекта — пусто.** Не писать `/health`.
3. **Путь проверки состояния:** `/health` (это URL, не папка).
4. Команда сборки:

```
pip3 install --upgrade -r /app/requirements.txt
```

5. Команда запуска:

```
uvicorn main:app --host 0.0.0.0 --port 80
```

6. Переменные только в панели Timeweb: `DATABASE_URL`, `ADMIN_PASSWORD`, `ADMIN_SECRET`, `UPLOAD_DIR=./uploads`, `MAX_FILE_MB=20`, `CORS_ORIGINS`, `FRAME_ANCESTORS`.

7. В Тильде, блок HTML (T123), код из `tilda/tilda-iframe-block.html`.

Админку в iframe не встраивать.

## Excel и фильтры

В админке таблица заявок, сортировка, фильтры и выгрузка Excel. Клик по строке открывает карточку.
