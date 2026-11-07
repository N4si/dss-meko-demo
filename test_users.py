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


if __name__ == "__main__":
    unittest.main()
