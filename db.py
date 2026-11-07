"""SQLite helpers for the practice repo."""
import sqlite3


def connect(path=":memory:"):
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
    conn.executemany(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        [("Ada Lovelace", "ada@example.com"), ("Alan Turing", "alan@example.com")],
    )
    conn.commit()
    return conn
