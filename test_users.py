import unittest

import db
import users


class GetUserTest(unittest.TestCase):
    def setUp(self):
        self.conn = db.connect()

    def tearDown(self):
        self.conn.close()

    def test_int_id_returns_matching_user(self):
        row = users.get_user(self.conn, 1).fetchone()
        self.assertEqual(row, (1, "Ada Lovelace", "ada@example.com"))

    def test_digit_string_id_returns_matching_user(self):
        row = users.get_user(self.conn, "2").fetchone()
        self.assertEqual(row, (2, "Alan Turing", "alan@example.com"))

    def test_missing_id_returns_no_rows(self):
        self.assertEqual(users.get_user(self.conn, 999).fetchall(), [])

    def test_injection_payload_is_treated_as_a_value(self):
        self.assertEqual(users.get_user(self.conn, "1 OR 1=1").fetchall(), [])

    def test_non_numeric_id_returns_no_rows(self):
        self.assertEqual(users.get_user(self.conn, "abc").fetchall(), [])


class GetUsersByEmailTest(unittest.TestCase):
    def setUp(self):
        self.conn = db.connect()

    def tearDown(self):
        self.conn.close()

    def test_existing_email_returns_matching_user(self):
        rows = users.get_users_by_email(self.conn, "ada@example.com").fetchall()
        self.assertEqual(rows, [(1, "Ada Lovelace", "ada@example.com")])

    def test_unknown_email_returns_no_rows(self):
        self.assertEqual(users.get_users_by_email(self.conn, "nobody@example.com").fetchall(), [])

    def test_injection_payload_is_treated_as_a_value(self):
        self.assertEqual(users.get_users_by_email(self.conn, "x' OR '1'='1").fetchall(), [])

    def test_shared_email_returns_all_matches_ordered_by_id(self):
        self.conn.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)", ("Alan Clone", "alan@example.com")
        )
        rows = users.get_users_by_email(self.conn, "alan@example.com").fetchall()
        self.assertEqual(
            rows,
            [(2, "Alan Turing", "alan@example.com"), (3, "Alan Clone", "alan@example.com")],
        )

    def test_match_is_case_sensitive(self):
        self.assertEqual(users.get_users_by_email(self.conn, "ADA@example.com").fetchall(), [])


if __name__ == "__main__":
    unittest.main()
