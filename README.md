# mashuk_forms

Анкета и админка семинара Машук.

Публичные формы:
- `/` — заявка «Образование на высоте»
- `/info` — данные участников того же семинара
- `/muni` — заявка «Межнациональные и межконфессиональные отношения в деятельности муниципалитетов»

Админка: `/admin`
АПИ заявок: `POST /apply`, `POST /info`, `POST /muni`
Проверка: `GET /health`

Регистрация на семинар муниципалитетов открыта. В форме один вариант дат:
13–16 ноября 2026 года (`tools/muni_strings.py`, ключ `s1d`).

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

7. В Тильде, блок HTML (T123):
   - заявка семинара: `tilda/tilda-iframe-block.html`
   - данные участников: `tilda/tilda-iframe-info.html`
   - заявка муниципалитетов: `tilda/tilda-iframe-muni.html`

Админку в iframe не встраивать.

## Excel и фильтры

### Скан паспорта в данных участника

На шаге 2 формы `/info` обязателен один скан страницы паспорта с фотографией:
PDF, JPG/JPEG или PNG, до 20 МБ (или меньшего лимита `MAX_FILE_MB`).
`POST /info` принимает multipart-поля `payload` (JSON) и `passport_scan` (файл).
Сервер проверяет расширение, сигнатуру формата и размер. Файл хранится в
`UPLOAD_DIR`, путь — в `participant_details.passport_scan_path`; колонка
добавляется автоматически при запуске, существующие анкеты остаются без скана.

В админке наличие скана отображается в списке и Excel. Скачать его можно
из карточки участника только с действующей сессией администратора. Публичные
ссылки на сканы не создаются. При ошибке записи анкеты новый файл удаляется.
Файл не сохраняется в черновике браузера; после перезагрузки его нужно выбрать заново.

На Timeweb `UPLOAD_DIR` должен находиться на постоянном хранилище, сохраняемом
между деплоями; это требуется и для ранее загруженных согласий.

Проверки: `pip install -r requirements-dev.txt`, затем
`python -m unittest discover -s tests -v`. Тесты используют временные файлы
и подменённое подключение к БД, не обращаясь к рабочей базе.

В админке таблица заявок, сортировка, фильтры и выгрузка Excel. Клик по строке открывает карточку.
