"""Regression coverage for the optional colleagues question. No live DB."""
import io
import json
import os
import time
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient
from openpyxl import load_workbook

with patch.dict(os.environ, {
    "DATABASE_URL": "", "ADMIN_PASSWORD": "test-only", "ADMIN_SECRET": "test-only",
}):
    import app
    import admin_api


class MunicipalColleaguesTests(unittest.TestCase):
    def setUp(self):
        env = patch.dict(os.environ, {
            "ADMIN_PASSWORD": "test-only", "ADMIN_SECRET": "test-only",
        })
        env.start()
        self.addCleanup(env.stop)
        self.client = TestClient(app.app)
        self.addCleanup(self.client.close)
        self.colleagues = "Иванов Иван, эксперт, +7 900 000-00-00"
        self.payload = {
            "fio": "Тест Тестов",
            "federal_district": app.DISTRICTS[0],
            "region": next(iter(app.REGIONS_SET)),
            "city": "Москва",
            "workplace": "Организация",
            "position": "Специалист",
            "birth_date": "1990-01-01",
            "snils": "test-snils",
            "inn": "test-inn",
            "phone": "+7 900 000-00-00",
            "email": "test@example.com",
            "stream": "17 — 20 октября 2026",
            "colleagues": self.colleagues,
        }

    def login(self):
        self.client.cookies.set(
            "mashuk_admin", admin_api._sign(str(int(time.time()) + 60))
        )

    def test_submission_persists_colleagues(self):
        with patch.object(app, "DATABASE_URL", "test-only"), \
             patch.object(app, "valid_snils", return_value=True), \
             patch.object(app, "valid_inn", return_value=True), \
             patch.object(app, "save_upload", return_value="consent/test.pdf"), \
             patch.object(app.psycopg, "connect") as connect:
            cursor = connect.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value
            cursor.fetchone.return_value = (42,)
            response = self.client.post(
                "/muni",
                data={"payload": json.dumps(self.payload)},
                files={"consent": ("consent.pdf", b"%PDF-1.4\n%%EOF")},
            )
        self.assertEqual(response.status_code, 200, response.text)
        sql, values = cursor.execute.call_args.args
        self.assertIn("colleagues", sql)
        self.assertEqual(values[app.MUNI_COLS.index("colleagues")], self.colleagues)

    def test_admin_card_and_excel_include_colleagues(self):
        self.login()
        item = {"id": 42, "fio": "Тест Тестов", "colleagues": self.colleagues,
                "consent_path": None, "payload_raw": self.payload}
        with patch.object(admin_api, "db"), \
             patch.object(admin_api, "as_dicts", return_value=[item]):
            card = self.client.get("/admin/api/municipal/42")
            excel = self.client.get("/admin/api/municipal/export.xlsx")
        self.assertEqual(card.status_code, 200, card.text)
        self.assertEqual(card.json()["colleagues"], self.colleagues)
        rows = list(load_workbook(io.BytesIO(excel.content)).active.values)
        headers = rows[0]
        column = headers.index("Коллеги, желающие участвовать")
        self.assertEqual(rows[1][column], self.colleagues)


if __name__ == "__main__":
    unittest.main()
