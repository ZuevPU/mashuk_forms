# -*- coding: utf-8 -*-
"""University seminar registration (Cultistudform). No live DB."""
import json
import os
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

with patch.dict(os.environ, {
    "DATABASE_URL": "", "UPLOAD_DIR": os.environ.get("TEMP", ".") + "/cultistud-test",
    "ADMIN_PASSWORD": "test-only", "ADMIN_SECRET": "test-only",
}):
    import app


class CultistudFormTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app.app)
        self.addCleanup(self.client.close)
        self.payload = {
            "fio": "Тест Тестов",
            "federal_district": app.DISTRICTS[0],
            "region": next(iter(app.REGIONS_SET)),
            "city": "Москва",
            "workplace": "МГУ",
            "position": "3 курс, история",
            "birth_date": "2000-01-01",
            "snils": "112-233-445 95",
            "inn": "500100732259",
            "phone": "+7 900 000-00-00",
            "email": "test@example.com",
        }

    def test_page_is_served_without_consent(self):
        import html as H

        r = self.client.get("/cultistudform")
        self.assertEqual(r.status_code, 200, r.text)
        text = H.unescape(r.text)
        self.assertIn("Заявка участника", text)
        self.assertIn("Студенческие сообщества", text)
        for name in ("fio", "federal_district", "region", "city", "workplace",
                     "position", "birth_date", "snils", "inn", "phone", "email"):
            self.assertIn('data-field="' + name + '"', r.text)
        self.assertNotIn('data-field="consent_confirm"', r.text)
        self.assertNotIn('name="consent"', r.text)

    def test_valid_submission_stores_fixed_stream(self):
        with patch.object(app, "DATABASE_URL", "test-only"), \
             patch.object(app.psycopg, "connect") as connect:
            cursor = connect.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value
            cursor.fetchone.return_value = (7,)
            r = self.client.post(
                "/cultistudform", data={"payload": json.dumps(self.payload, ensure_ascii=False)}
            )
        self.assertEqual(r.status_code, 200, r.text)
        sql, values = cursor.execute.call_args.args
        self.assertIn("cultistud_applications", sql)
        stored = dict(zip(app.CULTISTUD_COLS, values))
        self.assertEqual(stored["stream"], app.CULTISTUD_STREAM)
        self.assertEqual(stored["fio"], "Тест Тестов")
        self.assertEqual(stored["region"], self.payload["region"])

    def test_missing_field_is_rejected_before_database(self):
        for field in app.CULTISTUD_REQUIRED:
            with self.subTest(field=field), patch.object(app, "DATABASE_URL", "test-only"), \
                 patch.object(app.psycopg, "connect") as connect:
                payload = dict(self.payload)
                payload.pop(field)
                r = self.client.post(
                    "/cultistudform", data={"payload": json.dumps(payload, ensure_ascii=False)}
                )
                self.assertEqual(r.status_code, 400, r.text)
                self.assertEqual(r.json()["detail"], field + " required")
                connect.assert_not_called()

    def test_invalid_values_rejected(self):
        bad = {
            "region": ("Неизвестный регион", "region invalid"),
            "snils": ("123", "snils invalid"),
            "inn": ("123", "inn invalid"),
            "email": ("not-an-email", "email invalid"),
        }
        with patch.object(app, "DATABASE_URL", "test-only"), \
             patch.object(app.psycopg, "connect") as connect:
            for field, (value, detail) in bad.items():
                with self.subTest(field=field):
                    payload = dict(self.payload)
                    payload[field] = value
                    r = self.client.post(
                        "/cultistudform", data={"payload": json.dumps(payload, ensure_ascii=False)}
                    )
                    self.assertEqual(r.status_code, 400, r.text)
                    self.assertEqual(r.json()["detail"], detail)
            connect.assert_not_called()

    def test_broken_json_rejected(self):
        with patch.object(app, "DATABASE_URL", "test-only"):
            r = self.client.post("/cultistudform", data={"payload": "{"})
        self.assertEqual(r.status_code, 400)


if __name__ == "__main__":
    unittest.main()
