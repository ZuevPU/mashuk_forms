"""Run: python -m unittest discover -s tests -v (requires httpx). No live DB."""
import io
import json
import os
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import MagicMock, patch

_uploads = tempfile.TemporaryDirectory()
with patch.dict(os.environ, {
    "DATABASE_URL": "", "UPLOAD_DIR": _uploads.name,
    "ADMIN_PASSWORD": "test-only", "ADMIN_SECRET": "test-only",
}):
    import app
    import admin_api
from fastapi.testclient import TestClient
from openpyxl import load_workbook


class PassportUploadTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        for p in (
            patch.object(app, "UPLOAD_DIR", Path(self.directory.name)),
            patch.object(app, "DATABASE_URL", "test-only"),
            patch.dict(os.environ, {"ADMIN_PASSWORD": "test-only", "ADMIN_SECRET": "test-only"}),
        ):
            p.start()
            self.addCleanup(p.stop)
        self.client = TestClient(app.app)  # Do not run startup against a database.
        self.addCleanup(self.client.close)
        self.payload = dict(fio_latin="Test", gender="Test", citizenship="Test",
                            other_citizenships="No", stream="Test")
        self.content = b"%PDF-1.4\n%%EOF"

    def submit(self, name="passport.pdf", content=None):
        return self.client.post("/info", data={"payload": json.dumps(self.payload)},
                                files={"passport_scan": (name, self.content if content is None else content)})

    def test_valid_formats_and_database_path(self):
        for name, content in [("passport.pdf", self.content), ("passport.JPG", b"\xff\xd8\xffimage"),
                              ("passport.jpeg", b"\xff\xd8\xffimage"), ("passport.png", b"\x89PNG\r\n\x1a\nimage")]:
            with self.subTest(name=name), patch.object(app.psycopg, "connect") as connect:
                cursor = connect.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value
                cursor.fetchone.return_value = (7,)
                self.payload["passport_scan_path"] = "attacker-supplied-path"
                r = self.submit(name, content)
                self.assertEqual(r.status_code, 200, r.text)
                values = cursor.execute.call_args.args[1]
                stored = values[app.INFO_COLS.index("passport_scan_path")]
                self.assertNotEqual(stored, "attacker-supplied-path")
                self.assertEqual((Path(self.directory.name) / stored).read_bytes(), content)

    def test_invalid_files_rejected_before_database(self):
        with patch.object(app.psycopg, "connect") as connect:
            for name, content in [("x.exe", self.content), ("x.pdf", b"<html>"), ("x.png", self.content), ("x.pdf", b"")]:
                with self.subTest(name=name, content=content):
                    self.assertEqual(self.submit(name, content).status_code, 400)
            with patch.object(app, "MAX_BYTES", 8):
                self.assertEqual(self.submit().status_code, 400)
            self.assertEqual(self.client.post("/info", json=self.payload).status_code, 400)
            connect.assert_not_called()
            self.assertEqual(list(Path(self.directory.name).iterdir()), [])

    def test_database_failure_removes_uploaded_file(self):
        with patch.object(app.psycopg, "connect", side_effect=RuntimeError("test database failure")):
            self.assertEqual(self.submit().status_code, 500)
        self.assertEqual(list(Path(self.directory.name).iterdir()), [])

    def login(self):
        self.client.cookies.set("mashuk_admin", admin_api._sign(str(int(time.time()) + 60)))

    def test_download_requires_admin_even_with_file_token(self):
        with patch.object(admin_api, "db") as db:
            r = self.client.get("/admin/api/participants/7/file/passport?t=anything")
            self.assertEqual(r.status_code, 401)
            db.assert_not_called()

    def test_download_and_legacy_missing_file(self):
        self.login()
        path = Path(self.directory.name) / "scan.png"
        content = b"\x89PNG\r\n\x1a\nimage"
        path.write_bytes(content)
        with patch.object(admin_api, "db") as db, patch.object(admin_api, "find_upload", return_value=path):
            cursor = db.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value
            cursor.fetchone.return_value = (path.name, "Test Person")
            r = self.client.get("/admin/api/participants/7/file/passport")
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.content, content)
            self.assertEqual(r.headers["cache-control"], "no-store")
            self.assertIn("passport_Test_Person.png", r.headers["content-disposition"])
            cursor.fetchone.return_value = (None, "Legacy")
            self.assertEqual(self.client.get("/admin/api/participants/8/file/passport").status_code, 404)

    def test_card_hides_storage_path_and_handles_legacy(self):
        self.login()
        for value in (None, "scan.pdf"):
            with patch.object(admin_api, "db"), patch.object(admin_api, "as_dicts", return_value=[
                {"id": 7, "passport_scan_path": value, "payload_raw": {}}
            ]):
                item = self.client.get("/admin/api/participants/7").json()
                self.assertEqual(item["has_passport"], bool(value))
                self.assertNotIn("passport_scan_path", item)

    def test_excel_has_scan_status(self):
        self.login()
        with patch.object(admin_api, "db"), patch.object(admin_api, "as_dicts", return_value=[
            {"id": 7, "passport_scan_path": "scan.pdf"}, {"id": 8, "passport_scan_path": None}
        ]):
            r = self.client.get("/admin/api/participants/export.xlsx")
            self.assertEqual(r.status_code, 200)
            rows = list(load_workbook(io.BytesIO(r.content)).active.values)
            self.assertEqual([row[-1] for row in rows], ["Скан паспорта", "Да", "Нет"])


if __name__ == "__main__":
    unittest.main()
