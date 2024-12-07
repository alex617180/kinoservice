# utils/sqlite_to_postgres/db_manager.py

import sqlite3
import psycopg
from contextlib import contextmanager
from typing import Generator

@contextmanager
def sqlite_connection(db_path: str) -> Generator[sqlite3.Connection, None, None]:
    """ Context manager for SQLite connection. """
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.close()

@contextmanager
def postgres_connection(dsl: dict) -> Generator[psycopg.Connection, None, None]:
    """ Context manager for PostgreSQL connection. """
    conn = psycopg.connect(**dsl)
    try:
        yield conn
    finally:
        conn.close()
