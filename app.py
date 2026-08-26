import json
import logging
import os
import re
import uuid
from pathlib import Path
from urllib.parse import urlparse

import psycopg
from psycopg.types.json import Json
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware

from admin_api import primary_upload_dir, router as admin_router

load_dotenv()

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("mashuk")


def normalize_database_url(raw: str) -> str:
    s = (raw or "").strip().strip("'\"")
    if not s:
        return ""
    found = re.search(r"(postgres(?:ql)?://\S+)", s, re.I)
    if found:
        return found.group(1).rstrip("\"';")
    if s.lower().startswith("psql"):
        rest = s[4:].strip().strip("'\"")
        if rest:
            return normalize_database_url(rest)
        return ""
    return s


ROOT = Path(__file__).resolve().parent
DATABASE_URL = normalize_database_url(os.environ.get("DATABASE_URL", ""))
if DATABASE_URL:
    os.environ["DATABASE_URL"] = DATABASE_URL
UPLOAD_DIR = primary_upload_dir()
MAX_FILE_MB = int(os.environ.get("MAX_FILE_MB", "20"))
MAX_BYTES = MAX_FILE_MB * 1024 * 1024
FRAME_ANCESTORS = os.environ.get(
    "FRAME_ANCESTORS",
    "http://127.0.0.1:8000 http://localhost:8000 https://*.tilda.ws https://*.tilda.cc https://mashuk.online https://www.mashuk.online",
)
CORS_ORIGINS = [
    o.strip()
    for o in os.environ.get(
        "CORS_ORIGINS",
        "http://127.0.0.1:8000,http://localhost:8000,https://mashuk.online,https://www.mashuk.online",
    ).split(",")
    if o.strip()
]

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALWAYS_FRAME_ANCESTORS = [
    "https://*.tilda.ws",
    "https://*.tilda.cc",
    "https://mashuk.online",
    "https://www.mashuk.online",
]


def frame_ancestor_origin(token: str) -> str:
    token = token.strip().strip("'\"")
    if not token or token in ("self", "'self'"):
        return ""
    raw = token if "://" in token else "https://" + token
    parsed = urlparse(raw)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return ""
    return parsed.scheme + "://" + parsed.netloc


def frame_ancestors_header() -> str:
    origins = []
    for token in ALWAYS_FRAME_ANCESTORS + FRAME_ANCESTORS.split():
        origin = frame_ancestor_origin(token)
        if origin and origin not in origins:
            origins.append(origin)
    return "frame-ancestors 'self' " + " ".join(origins)


class FrameAncestorsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if request.url.path.startswith("/admin"):
            response.headers["Content-Security-Policy"] = "frame-ancestors 'self'"
        else:
            response.headers["Content-Security-Policy"] = frame_ancestors_header()
        if "x-frame-options" in response.headers:
            del response.headers["x-frame-options"]
        return response


app = FastAPI(title="Mashuk seminar applications", docs_url=None, redoc_url=None)
app.add_middleware(FrameAncestorsMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["POST", "OPTIONS", "GET"],
    allow_headers=["*"],
    max_age=86400,
)


def init_schema() -> None:
    if not DATABASE_URL:
        log.warning("DATABASE_URL is empty")
        return
    schema = (ROOT / "schema.sql").read_text(encoding="utf-8")
    statements = [s.strip() for s in schema.split(";") if s.strip()]
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            for stmt in statements:
                cur.execute(stmt)
        conn.commit()
    log.info("schema ready")


@app.on_event("startup")
def on_startup():
    try:
        init_schema()
    except Exception:
        log.exception("schema init failed")
    log.info("uploads dir %s exists=%s", UPLOAD_DIR, UPLOAD_DIR.is_dir())


def save_upload(kind: str, upload: UploadFile, allowed: set[str]) -> str:
    if not upload or not upload.filename:
        raise HTTPException(400, f"missing file: {kind}")
    suffix = Path(upload.filename).suffix.lower()
    if suffix not in allowed:
        raise HTTPException(400, f"bad file type for {kind}")
    data = upload.file.read()
    if not data:
        raise HTTPException(400, f"empty file: {kind}")
    if len(data) > MAX_BYTES:
        raise HTTPException(400, f"file too large: {kind}")
    name = f"{uuid.uuid4().hex}_{kind}{suffix}"
    path = UPLOAD_DIR / name
    path.write_bytes(data)
    return name


@app.get("/health")
def health():
    db_ok = False
    db_error = None
    if DATABASE_URL:
        try:
            with psycopg.connect(DATABASE_URL, connect_timeout=5) as conn:
                conn.execute("SELECT 1")
            db_ok = True
        except Exception as exc:
            db_error = str(exc)
    return {"ok": True, "db": db_ok, "db_error": db_error}


INFO_COLS = [
    "fio_latin",
    "health_limits",
    "meal_type",
    "id_doc_type",
    "id_doc_series",
    "id_doc_number",
    "id_doc_issued",
    "id_doc_valid_from",
    "id_doc_valid_to",
    "id_doc_issuer",
    "entry_doc_name",
    "entry_doc_series",
    "entry_doc_number",
    "entry_doc_issued",
    "entry_doc_valid_from",
    "entry_doc_valid_to",
    "entry_doc_issuer",
    "stream",
    "depart_country",
    "depart_city",
    "return_ticket",
    "baggage",
    "visa_needed",
    "transit_visa",
    "agree_tickets",
    "agree_notice",
    "agree_truth",
    "agree_extra_docs",
    "agree_refusal",
    "payload_raw",
]


def as_yes_no(value) -> str:
    if value is True:
        return "\u0434\u0430"
    if value is False or value is None:
        return "\u043d\u0435\u0442"
    text = str(value).strip().lower()
    if text in ("1", "true", "yes", "da", "\u0434\u0430"):
        return "\u0434\u0430"
    return "\u043d\u0435\u0442"


@app.get("/")
def index():
    path = ROOT / "static" / "index.html"
    if not path.exists():
        path = ROOT / "tilda" / "preview-apply.html"
    if not path.exists():
        raise HTTPException(404, "frontend is missing")
    return FileResponse(path, media_type="text/html; charset=utf-8")


@app.get("/info")
@app.get("/info/")
def info_page():
    path = ROOT / "static" / "info.html"
    if not path.exists():
        raise HTTPException(404, "info form is missing")
    return FileResponse(path, media_type="text/html; charset=utf-8")


@app.get("/admin")
@app.get("/admin/")
def admin_page():
    path = ROOT / "static" / "admin.html"
    if not path.exists():
        raise HTTPException(404, "admin frontend is missing")
    return FileResponse(
        path,
        media_type="text/html; charset=utf-8",
        headers={"Cache-Control": "no-store"},
    )


app.include_router(admin_router, prefix="/admin")


@app.get("/consent-template")
def consent_template():
    src_docx = ROOT / "consent" / "consent-source.docx"
    if src_docx.exists():
        return FileResponse(
            src_docx,
            filename="Soglasie_shablon.docx",
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    txt = ROOT / "consent" / "consent-text.txt"
    body = txt.read_text(encoding="utf-8") if txt.exists() else ""
    paras = []
    for line in body.splitlines():
        safe = (
            line.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        paras.append("<p>" + (safe or "&nbsp;") + "</p>")
    html = (
        "<html xmlns:o='urn:schemas-microsoft-com:office:office' "
        "xmlns:w='urn:schemas-microsoft-com:office:word'>"
        "<head><meta charset='utf-8'></head><body>"
        + "".join(paras)
        + "</body></html>"
    )
    return Response(
        content=("\ufeff" + html).encode("utf-8"),
        media_type="application/msword",
        headers={"Content-Disposition": 'attachment; filename="Soglasie_shablon.doc"'},
    )


@app.post("/apply")
def apply(
    payload: str = Form(...),
    portfolio: UploadFile = File(...),
    consent: UploadFile = File(...),
):
    if not DATABASE_URL:
        raise HTTPException(500, "DATABASE_URL is not set")
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        raise HTTPException(400, "payload must be JSON")
    if not isinstance(data, dict):
        raise HTTPException(400, "payload must be an object")
    if not str(data.get("email") or "").strip():
        raise HTTPException(400, "email required")
    if not str(data.get("fio_latin") or "").strip():
        raise HTTPException(400, "fio_latin required")

    portfolio_path = save_upload("portfolio", portfolio, {".pdf"})
    consent_path = save_upload(
        "consent",
        consent,
        {".pdf", ".jpg", ".jpeg", ".png", ".doc", ".docx"},
    )

    cols = [
        "program",
        "fio_latin",
        "fio_ru",
        "birth_date",
        "gender",
        "country",
        "city",
        "arrival",
        "citizenship",
        "all_citizenships",
        "phone",
        "email",
        "messenger",
        "messenger_link",
        "messenger_other",
        "org_name",
        "org_spec",
        "org_location",
        "position",
        "audience",
        "audience_other",
        "stream",
        "how_learned",
        "intl_programs",
        "intl_details",
        "ru_programs",
        "ru_details",
        "why",
        "coop",
        "mentor",
        "directions",
        "directions_other",
        "address",
        "passport_series",
        "passport_number",
        "passport_date",
        "passport_issued",
        "portfolio_path",
        "consent_path",
        "payload_raw",
    ]
    values = []
    for col in cols:
        if col == "portfolio_path":
            values.append(portfolio_path)
        elif col == "consent_path":
            values.append(consent_path)
        elif col == "payload_raw":
            values.append(Json(data))
        elif col in ("messenger", "audience", "directions"):
            values.append(Json(data.get(col) or []))
        else:
            val = data.get(col)
            if isinstance(val, (list, dict)):
                values.append(json.dumps(val, ensure_ascii=False))
            else:
                values.append(None if val is None else str(val))

    placeholders = ", ".join(["%s"] * len(cols))
    sql = (
        "INSERT INTO seminar_applications ("
        + ", ".join(cols)
        + ") VALUES ("
        + placeholders
        + ") RETURNING id"
    )
    try:
        with psycopg.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, values)
                row = cur.fetchone()
            conn.commit()
    except Exception:
        log.exception("insert failed")
        raise HTTPException(500, "database error")

    return JSONResponse({"ok": True, "id": row[0] if row else None})


@app.post("/info")
async def info_submit(request: Request):
    if not DATABASE_URL:
        raise HTTPException(500, "DATABASE_URL is not set")
    ctype = (request.headers.get("content-type") or "").lower()
    try:
        if "application/json" in ctype:
            data = await request.json()
        else:
            form = await request.form()
            data = json.loads(str(form.get("payload") or "{}"))
    except Exception:
        raise HTTPException(400, "payload must be JSON")
    if not isinstance(data, dict):
        raise HTTPException(400, "payload must be an object")
    if not str(data.get("fio_latin") or "").strip():
        raise HTTPException(400, "fio_latin required")
    if not str(data.get("stream") or "").strip():
        raise HTTPException(400, "stream required")

    bool_cols = {
        "agree_tickets",
        "agree_notice",
        "agree_truth",
        "agree_extra_docs",
        "agree_refusal",
    }
    values = []
    for col in INFO_COLS:
        if col == "payload_raw":
            values.append(Json(data))
            continue
        val = data.get(col)
        if col in bool_cols:
            values.append(as_yes_no(val))
        elif isinstance(val, (list, dict)):
            values.append(json.dumps(val, ensure_ascii=False))
        else:
            values.append(None if val is None else str(val).strip())

    placeholders = ", ".join(["%s"] * len(INFO_COLS))
    sql = (
        "INSERT INTO participant_details ("
        + ", ".join(INFO_COLS)
        + ") VALUES ("
        + placeholders
        + ") RETURNING id"
    )
    try:
        with psycopg.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, values)
                row = cur.fetchone()
            conn.commit()
    except Exception:
        log.exception("info insert failed")
        raise HTTPException(500, "database error")

    return JSONResponse({"ok": True, "id": row[0] if row else None})
