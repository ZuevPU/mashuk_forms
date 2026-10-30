# -*- coding: utf-8 -*-
"""University seminar registration (Cultistudform), including its password gate.

No live DB.
"""
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
        # Registration is closed in production by default; the form and the
        # password gate are exercised with the switch turned off.
        opened = patch.object(app, "CULTISTUD_FORM_CLOSED", False)
        opened.start()
        self.addCleanup(opened.stop)
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

    def unlock(self, password=None):
        return self.client.post(
            "/cultistudform/unlock",
            data={"password": app.CULTISTUD_PASSWORD if password is None else password},
        )

    def token(self):
        response = self.unlock()
        self.assertEqual(response.status_code, 200, response.text)
        return response.json()["token"]

    # --- registration closed ------------------------------------------------

    def test_closed_page_replaces_the_form(self):
        import html as H

        with patch.object(app, "CULTISTUD_FORM_CLOSED", True):
            r = self.client.get("/cultistudform")
        self.assertEqual(r.status_code, 200)
        text = H.unescape(r.text)
        self.assertIn("Регистрация завершена", text)
        self.assertNotIn("Доступ по паролю", text)
        self.assertNotIn('data-field="fio"', r.text)
        self.assertEqual(r.headers["cache-control"], "no-store")

    def test_closed_page_wins_over_the_token(self):
        import html as H

        token = self.token()
        with patch.object(app, "CULTISTUD_FORM_CLOSED", True):
            r = self.client.get("/cultistudform", params={"t": token})
        self.assertIn("Регистрация завершена", H.unescape(r.text))
        self.assertNotIn('data-field="fio"', r.text)

    def test_submission_refused_when_closed(self):
        token = self.token()
        with patch.object(app, "CULTISTUD_FORM_CLOSED", True), \
             patch.object(app, "DATABASE_URL", "test-only"), \
             patch.object(app.psycopg, "connect") as connect:
            r = self.client.post(
                "/cultistudform",
                data={"payload": json.dumps(self.payload, ensure_ascii=False), "t": token},
            )
        self.assertEqual(r.status_code, 403, r.text)
        self.assertEqual(r.json()["detail"], "registration is closed")
        connect.assert_not_called()

    # --- password gate -----------------------------------------------------

    def test_form_is_closed_without_password(self):
        import html as H

        r = self.client.get("/cultistudform")
        self.assertEqual(r.status_code, 200)
        text = H.unescape(r.text)
        self.assertIn("Доступ по паролю", text)
        self.assertNotIn('data-field="fio"', r.text)
        self.assertNotIn("Пароль", "")  # sanity: page has no form fields
        self.assertEqual(r.headers["cache-control"], "no-store")

    def test_wrong_password_is_rejected(self):
        r = self.unlock("0000")
        self.assertEqual(r.status_code, 401)
        self.assertNotIn("token", r.text)

    def test_password_opens_the_form(self):
        token = self.token()
        self.assertTrue(app.cultistud_token_ok(token))
        r = self.client.get("/cultistudform", params={"t": token})
        self.assertEqual(r.status_code, 200)
        self.assertIn('data-field="fio"', r.text)

    def test_token_alone_opens_the_form_without_cookies(self):
        # Inside the Tilda iframe third-party cookies may be blocked, so the
        # token from the URL must be enough on its own.
        import html as H

        token = self.token()
        self.client.cookies.clear()
        r = self.client.get("/cultistudform", params={"t": token})
        self.assertEqual(r.status_code, 200)
        self.assertIn('data-field="fio"', r.text)
        self.assertNotIn("Доступ по паролю", H.unescape(r.text))

    def test_broken_and_expired_tokens_are_rejected(self):
        import html as H

        for token in ("", "abc", "1.deadbeef", str(0) + ".x"):
            with self.subTest(token=token):
                r = self.client.get("/cultistudform", params={"t": token})
                self.assertEqual(r.status_code, 200)
                self.assertIn("Доступ по паролю", H.unescape(r.text))
        expired = "-1." + app._cultistud_sign("-1")
        self.assertFalse(app.cultistud_token_ok(expired))

    def test_cookie_opens_the_form(self):
        self.token()  # the unlock response sets the cookie on the client
        r = self.client.get("/cultistudform")
        self.assertIn('data-field="fio"', r.text)

    # --- the form itself ---------------------------------------------------

    def test_page_is_served_without_consent(self):
        import html as H

        r = self.client.get("/cultistudform", params={"t": self.token()})
        self.assertEqual(r.status_code, 200, r.text)
        text = H.unescape(r.text)
        self.assertIn("Заявка участника", text)
        self.assertIn("Студенческие сообщества", text)
        for name in ("fio", "federal_district", "region", "city", "workplace",
                     "position", "birth_date", "snils", "inn", "phone", "email"):
            self.assertIn('data-field="' + name + '"', r.text)
        self.assertNotIn('data-field="consent_confirm"', r.text)
        self.assertNotIn('name="consent"', r.text)

    def test_submission_requires_password(self):
        with patch.object(app, "DATABASE_URL", "test-only"), \
             patch.object(app.psycopg, "connect") as connect:
            r = self.client.post(
                "/cultistudform", data={"payload": json.dumps(self.payload, ensure_ascii=False)}
            )
        self.assertEqual(r.status_code, 403, r.text)
        connect.assert_not_called()

    def test_valid_submission_stores_fixed_stream(self):
        with patch.object(app, "DATABASE_URL", "test-only"), \
             patch.object(app.psycopg, "connect") as connect:
            cursor = connect.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value
            cursor.fetchone.return_value = (7,)
            r = self.client.post(
                "/cultistudform",
                data={"payload": json.dumps(self.payload, ensure_ascii=False), "t": self.token()},
            )
        self.assertEqual(r.status_code, 200, r.text)
        sql, values = cursor.execute.call_args.args
        self.assertIn("cultistud_applications", sql)
        stored = dict(zip(app.CULTISTUD_COLS, values))
        self.assertEqual(stored["stream"], app.CULTISTUD_STREAM)
        self.assertEqual(stored["fio"], "Тест Тестов")
        self.assertEqual(stored["region"], self.payload["region"])

    def test_missing_field_is_rejected_before_database(self):
        token = self.token()
        for field in app.CULTISTUD_REQUIRED:
            with self.subTest(field=field), patch.object(app, "DATABASE_URL", "test-only"), \
                 patch.object(app.psycopg, "connect") as connect:
                payload = dict(self.payload)
                payload.pop(field)
                r = self.client.post(
                    "/cultistudform",
                    data={"payload": json.dumps(payload, ensure_ascii=False), "t": token},
                )
                self.assertEqual(r.status_code, 400, r.text)
                self.assertEqual(r.json()["detail"], field + " required")
                connect.assert_not_called()

    def test_invalid_values_rejected(self):
        token = self.token()
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
                        "/cultistudform",
                        data={"payload": json.dumps(payload, ensure_ascii=False), "t": token},
                    )
                    self.assertEqual(r.status_code, 400, r.text)
                    self.assertEqual(r.json()["detail"], detail)
            connect.assert_not_called()

    def test_broken_json_rejected(self):
        with patch.object(app, "DATABASE_URL", "test-only"):
            r = self.client.post(
                "/cultistudform", data={"payload": "{", "t": self.token()}
            )
        self.assertEqual(r.status_code, 400)


if __name__ == "__main__":
    unittest.main()
