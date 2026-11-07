"""User lookups."""


def get_user(db, user_id):
    return db.execute("SELECT * FROM users WHERE id = ?", (user_id,))


def get_users_by_email(db, email):
    """Return a cursor over every user whose email equals ``email``, ordered by id.

    Matching is exact and case-sensitive: the email is neither lowercased nor
    trimmed. Emails are not unique, so callers may get several rows.
    """
    return db.execute("SELECT * FROM users WHERE email = ? ORDER BY id", (email,))
