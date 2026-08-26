import hashlib
import hmac
import json
import os
import time
from io import BytesIO
from pathlib import Path
from typing import Optional

import psycopg
from fastapi import APIRouter, Cookie, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, Response
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

COOKIE = "mashuk_admin"
SORTABLE = {
    "id": "id",
    "created_at": "created_at",
    "fio_latin": "fio_latin",
    "fio_ru": "fio_ru",
    "email": "email",
    "phone": "phone",
    "country": "country",
    "city": "city",
    "org_name": "org_name",
    "stream": "stream",
}

EXCEL_COLUMNS = [
    ("id", "ID"),
    ("created_at", "\u0414\u0430\u0442\u0430 \u043f\u043e\u0434\u0430\u0447\u0438"),
    ("fio_latin", "\u0424\u0418\u041e (passport)"),
    ("fio_ru", "\u0424\u0418\u041e \u0440\u0443\u0441."),
    ("birth_date", "\u0414\u0430\u0442\u0430 \u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f"),
    ("gender", "\u041f\u043e\u043b"),
    ("country", "\u0421\u0442\u0440\u0430\u043d\u0430"),
    ("city", "\u0413\u043e\u0440\u043e\u0434"),
    ("arrival", "\u041e\u0442\u043a\u0443\u0434\u0430 \u043f\u0440\u0438\u0431\u044b\u0432\u0430\u0435\u0442"),
    ("citizenship", "\u0413\u0440\u0430\u0436\u0434\u0430\u043d\u0441\u0442\u0432\u043e"),
    ("all_citizenships", "\u0412\u0441\u0435 \u0433\u0440\u0430\u0436\u0434\u0430\u043d\u0441\u0442\u0432\u0430"),
    ("phone", "\u0422\u0435\u043b\u0435\u0444\u043e\u043d"),
    ("email", "E-mail"),
    ("messenger", "\u041c\u0435\u0441\u0441\u0435\u043d\u0434\u0436\u0435\u0440"),
    ("messenger_link", "\u0421\u0441\u044b\u043b\u043a\u0430 \u043c\u0435\u0441\u0441\u0435\u043d\u0434\u0436\u0435\u0440\u0430"),
    ("messenger_other", "\u0414\u0440\u0443\u0433\u043e\u0439 \u043c\u0435\u0441\u0441\u0435\u043d\u0434\u0436\u0435\u0440"),
    ("org_name", "\u041e\u0440\u0433\u0430\u043d\u0438\u0437\u0430\u0446\u0438\u044f"),
    ("org_spec", "\u0421\u043f\u0435\u0446\u0438\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u044f"),
    ("org_location", "\u0421\u0442\u0440\u0430\u043d\u0430 \u0438 \u0433\u043e\u0440\u043e\u0434 \u043e\u0440\u0433\u0430\u043d\u0438\u0437\u0430\u0446\u0438\u0438"),
    ("position", "\u0414\u043e\u043b\u0436\u043d\u043e\u0441\u0442\u044c"),
    ("audience", "\u0410\u0443\u0434\u0438\u0442\u043e\u0440\u0438\u044f"),
    ("audience_other", "\u0410\u0443\u0434\u0438\u0442\u043e\u0440\u0438\u044f (\u0434\u0440\u0443\u0433\u043e\u0435)"),
    ("stream", "\u041f\u043e\u0442\u043e\u043a"),
    ("how_learned", "\u041e\u0442\u043a\u0443\u0434\u0430 \u0443\u0437\u043d\u0430\u043b"),
    ("intl_programs", "\u041c\u0435\u0436\u0434\u0443\u043d\u0430\u0440\u043e\u0434\u043d\u044b\u0435 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u044b"),
    ("intl_details", "\u041c\u0435\u0436\u0434\u0443\u043d\u0430\u0440\u043e\u0434\u043d\u044b\u0435 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u044b (\u0434\u0435\u0442\u0430\u043b\u0438)"),
    ("ru_programs", "\u0420\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u0438\u0435 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u044b"),
    ("ru_details", "\u0420\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u0438\u0435 \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u044b (\u0434\u0435\u0442\u0430\u043b\u0438)"),
    ("why", "\u041f\u043e\u0447\u0435\u043c\u0443 \u0432\u0430\u0436\u043d\u043e \u0443\u0447\u0430\u0441\u0442\u0438\u0435"),
    ("coop", "\u041f\u0440\u0435\u0434\u043b\u043e\u0436\u0435\u043d\u0438\u0435 \u043f\u043e \u0441\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u0447\u0435\u0441\u0442\u0432\u0443"),
    ("mentor", "\u041d\u0430\u0441\u0442\u0430\u0432\u043d\u0438\u043a"),
    ("directions", "\u041d\u0430\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u044f"),
    ("directions_other", "\u041d\u0430\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435 (\u0434\u0440\u0443\u0433\u043e\u0435)"),
    ("address", "\u0410\u0434\u0440\u0435\u0441 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438"),
    ("passport_series", "\u041f\u0430\u0441\u043f\u043e\u0440\u0442: \u0441\u0435\u0440\u0438\u044f"),
    ("passport_number", "\u041f\u0430\u0441\u043f\u043e\u0440\u0442: \u043d\u043e\u043c\u0435\u0440"),
    ("passport_date", "\u041f\u0430\u0441\u043f\u043e\u0440\u0442: \u0434\u0430\u0442\u0430"),
    ("passport_issued", "\u041f\u0430\u0441\u043f\u043e\u0440\u0442: \u043a\u0435\u043c \u0432\u044b\u0434\u0430\u043d"),
    ("has_portfolio", "\u041f\u043e\u0440\u0442\u0444\u043e\u043b\u0438\u043e"),
    ("has_consent", "\u0421\u043e\u0433\u043b\u0430\u0441\u0438\u0435"),
]


def _password() -> str:
    return os.environ.get("ADMIN_PASSWORD", "").strip()


def _secret() -> bytes:
    raw = os.environ.get("ADMIN_SECRET", "").strip() or _password() or "mashuk-dev"
    return raw.encode("utf-8")


def _sign(payload: str) -> str:
    sig = hmac.new(_secret(), payload.encode("utf-8"), hashlib.sha256).hexdigest()
    return payload + "." + sig


def _check_token(token: Optional[str]) -> bool:
    if not token or "." not in token:
        return False
    payload, sig = token.rsplit(".", 1)
    expect = hmac.new(_secret(), payload.encode("utf-8"), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expect, sig):
        return False
    try:
        exp = int(payload)
    except ValueError:
        return False
    return exp >= int(time.time())


def require_admin(mashuk_admin: Optional[str] = Cookie(default=None)):
    if not _password():
        raise HTTPException(503, "ADMIN_PASSWORD is not set")
    if not _check_token(mashuk_admin):
        raise HTTPException(401, "unauthorized")
    return True


def db():
    url = os.environ.get("DATABASE_URL", "").strip()
    if not url:
        raise HTTPException(500, "DATABASE_URL is not set")
    return psycopg.connect(url)


def as_dicts(cur):
    cols = [d.name for d in cur.description]
    out = []
    for row in cur.fetchall():
        item = {}
        for k, v in zip(cols, row):
            if hasattr(v, "isoformat"):
                item[k] = v.isoformat()
            else:
                item[k] = v
        out.append(item)
    return out


def cell(v) -> str:
    if v is None:
        return ""
    if isinstance(v, (list, dict)):
        if isinstance(v, list):
            return ", ".join(str(x) for x in v)
        return json.dumps(v, ensure_ascii=False)
    if hasattr(v, "isoformat"):
        return v.isoformat()
    return str(v)


def parse_filters(request: Request):
    q = request.query_params
    return {
        "q": (q.get("q") or "").strip(),
        "stream": (q.get("stream") or "").strip(),
        "country": (q.get("country") or "").strip(),
        "gender": (q.get("gender") or "").strip(),
        "date_from": (q.get("date_from") or "").strip(),
        "date_to": (q.get("date_to") or "").strip(),
        "sort": SORTABLE.get(q.get("sort") or "created_at", "created_at"),
        "order": "ASC" if (q.get("order") or "").lower() == "asc" else "DESC",
        "page": max(1, int(q.get("page") or 1)),
        "limit": min(100, max(10, int(q.get("limit") or 50))),
    }


def where_sql(f):
    clauses = ["TRUE"]
    args = []
    if f["q"]:
        like = "%" + f["q"] + "%"
        clauses.append(
            "("
            "fio_latin ILIKE %s OR fio_ru ILIKE %s OR email ILIKE %s OR phone ILIKE %s "
            "OR country ILIKE %s OR city ILIKE %s OR org_name ILIKE %s OR citizenship ILIKE %s"
            ")"
        )
        args.extend([like] * 8)
    if f["stream"]:
        clauses.append("stream = %s")
        args.append(f["stream"])
    if f["country"]:
        clauses.append("country ILIKE %s")
        args.append("%" + f["country"] + "%")
    if f["gender"]:
        clauses.append("gender = %s")
        args.append(f["gender"])
    if f["date_from"]:
        clauses.append("created_at::date >= %s")
        args.append(f["date_from"])
    if f["date_to"]:
        clauses.append("created_at::date <= %s")
        args.append(f["date_to"])
    return " AND ".join(clauses), args


router = APIRouter()


@router.post("/api/login")
async def login(request: Request):
    pwd = _password()
    if not pwd:
        raise HTTPException(503, "ADMIN_PASSWORD is not set")
    try:
        body = await request.json()
    except Exception:
        body = {}
    given = str((body or {}).get("password") or "")
    given_h = hashlib.sha256(given.encode("utf-8")).digest()
    pwd_h = hashlib.sha256(pwd.encode("utf-8")).digest()
    if not hmac.compare_digest(given_h, pwd_h):
        raise HTTPException(401, "bad password")
    token = _sign(str(int(time.time()) + 7 * 24 * 3600))
    response = JSONResponse({"ok": True})
    response.set_cookie(
        COOKIE,
        token,
        httponly=True,
        samesite="lax",
        max_age=7 * 24 * 3600,
        path="/",
    )
    return response


@router.post("/api/logout")
def logout():
    response = JSONResponse({"ok": True})
    response.delete_cookie(COOKIE, path="/")
    return response


@router.get("/api/me")
def me(mashuk_admin: Optional[str] = Cookie(default=None)):
    require_admin(mashuk_admin)
    return {"ok": True}


@router.get("/api/meta")
def meta(mashuk_admin: Optional[str] = Cookie(default=None)):
    require_admin(mashuk_admin)
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) FROM seminar_applications"
            )
            total = cur.fetchone()[0]
            cur.execute(
                "SELECT DISTINCT stream FROM seminar_applications "
                "WHERE stream IS NOT NULL AND stream <> '' ORDER BY 1"
            )
            streams = [r[0] for r in cur.fetchall()]
            cur.execute(
                "SELECT DISTINCT country FROM seminar_applications "
                "WHERE country IS NOT NULL AND country <> '' ORDER BY 1"
            )
            countries = [r[0] for r in cur.fetchall()]
            cur.execute(
                "SELECT DISTINCT gender FROM seminar_applications "
                "WHERE gender IS NOT NULL AND gender <> '' ORDER BY 1"
            )
            genders = [r[0] for r in cur.fetchall()]
    return {
        "total": total,
        "streams": streams,
        "countries": countries,
        "genders": genders,
    }


@router.get("/api/applications")
def list_applications(request: Request, mashuk_admin: Optional[str] = Cookie(default=None)):
    require_admin(mashuk_admin)
    f = parse_filters(request)
    where, args = where_sql(f)
    offset = (f["page"] - 1) * f["limit"]
    sql_count = f"SELECT COUNT(*) FROM seminar_applications WHERE {where}"
    sql = (
        "SELECT id, created_at, fio_latin, fio_ru, email, phone, country, city, "
        "org_name, position, stream, gender, citizenship, "
        "(portfolio_path IS NOT NULL AND portfolio_path <> '') AS has_portfolio, "
        "(consent_path IS NOT NULL AND consent_path <> '') AS has_consent "
        f"FROM seminar_applications WHERE {where} "
        f"ORDER BY {f['sort']} {f['order']} NULLS LAST "
        "LIMIT %s OFFSET %s"
    )
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute(sql_count, args)
            total = cur.fetchone()[0]
            cur.execute(sql, args + [f["limit"], offset])
            items = as_dicts(cur)
    return {
        "items": items,
        "total": total,
        "page": f["page"],
        "limit": f["limit"],
        "pages": max(1, (total + f["limit"] - 1) // f["limit"]),
        "sort": f["sort"],
        "order": f["order"].lower(),
    }


@router.get("/api/applications/export.xlsx")
def export_xlsx(request: Request, mashuk_admin: Optional[str] = Cookie(default=None)):
    require_admin(mashuk_admin)
    f = parse_filters(request)
    where, args = where_sql(f)
    sql = (
        "SELECT *, "
        "(portfolio_path IS NOT NULL AND portfolio_path <> '') AS has_portfolio, "
        "(consent_path IS NOT NULL AND consent_path <> '') AS has_consent "
        f"FROM seminar_applications WHERE {where} ORDER BY {f['sort']} {f['order']} NULLS LAST"
    )
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, args)
            rows = as_dicts(cur)
    yes = "\u0434\u0430"
    no = "\u043d\u0435\u0442"
    for row in rows:
        row["has_portfolio"] = yes if row.get("has_portfolio") else no
        row["has_consent"] = yes if row.get("has_consent") else no
    wb = Workbook()
    ws = wb.active
    ws.title = "Zayavki"
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill("solid", fgColor="223F9A")
    for i, (_key, title) in enumerate(EXCEL_COLUMNS, 1):
        cell_ref = ws.cell(1, i, title)
        cell_ref.font = header_font
        cell_ref.fill = header_fill
        cell_ref.alignment = Alignment(wrap_text=True, vertical="center")
    for r_i, row in enumerate(rows, 2):
        for c_i, (key, _title) in enumerate(EXCEL_COLUMNS, 1):
            ws.cell(r_i, c_i, cell(row.get(key)))
    ws.auto_filter.ref = f"A1:{get_column_letter(len(EXCEL_COLUMNS))}{max(1, len(rows)+1)}"
    ws.freeze_panes = "A2"
    for i in range(1, len(EXCEL_COLUMNS) + 1):
        ws.column_dimensions[get_column_letter(i)].width = 22
    buf = BytesIO()
    wb.save(buf)
    filename = "mashuk_zayavki.xlsx"
    return Response(
        content=buf.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/api/applications/{app_id}")
def get_application(app_id: int, mashuk_admin: Optional[str] = Cookie(default=None)):
    require_admin(mashuk_admin)
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM seminar_applications WHERE id = %s", (app_id,)
            )
            items = as_dicts(cur)
    if not items:
        raise HTTPException(404, "not found")
    item = items[0]
    item["has_portfolio"] = bool(item.get("portfolio_path"))
    item["has_consent"] = bool(item.get("consent_path"))
    item.pop("portfolio_path", None)
    item.pop("consent_path", None)
    return item


def _safe_file(stored: str, upload_dir: Path) -> Path:
    path = Path(stored)
    if not path.is_absolute():
        path = (upload_dir / path).resolve()
    else:
        path = path.resolve()
    root = upload_dir.resolve()
    if root not in path.parents and path != root:
        raise HTTPException(404, "file not found")
    if not path.exists() or not path.is_file():
        raise HTTPException(404, "file not found")
    return path


@router.get("/api/applications/{app_id}/file/{kind}")
def get_file(
    app_id: int,
    kind: str,
    mashuk_admin: Optional[str] = Cookie(default=None),
):
    require_admin(mashuk_admin)
    if kind not in ("portfolio", "consent"):
        raise HTTPException(404, "unknown file")
    col = "portfolio_path" if kind == "portfolio" else "consent_path"
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"SELECT {col} FROM seminar_applications WHERE id = %s",
                (app_id,),
            )
            row = cur.fetchone()
    if not row or not row[0]:
        raise HTTPException(404, "file not found")
    upload_dir = Path(os.environ.get("UPLOAD_DIR", "./uploads")).resolve()
    path = _safe_file(row[0], upload_dir)
    return FileResponse(path, filename=path.name)
