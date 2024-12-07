# utils/sqlite_to_postgres/run.py

import sqlite3
from contextlib import closing
from psycopg.rows import dict_row
from utils.sqlite_to_postgres.db_manager import sqlite_connection, postgres_connection
from utils.sqlite_to_postgres.data_transfer import DataTransfer
from utils.sqlite_to_postgres.models import Genre, Person, FilmWork, GenreFilmWork, PersonFilmWork

def run_migration(sqlite_db_path: str, dls_postgres: dict):
    """
    Migrate data from SQLite to PostgreSQL with testing.

    Args:
        sqlite_db_path (str): Path to SQLite database.
        dls_postgres (dict): DLS for PostgreSQL.
    """
    tables = [
        ("genre", Genre),
        ("person", Person),
        ("film_work", FilmWork),
        ("genre_film_work", GenreFilmWork),
        ("person_film_work", PersonFilmWork),
    ]

    with sqlite_connection(sqlite_db_path) as sqlite_conn, postgres_connection(dls_postgres) as postgres_conn:
        sqlite_conn.row_factory = sqlite3.Row
        with closing(sqlite_conn.cursor()) as sqlite_cur, closing(postgres_conn.cursor(row_factory=dict_row)) as postgres_cur:

            data_transfer = DataTransfer(sqlite_cur, postgres_cur, postgres_conn)

            for table_name, model_cls in tables:
                data_transfer.transfer_table(table_name, model_cls)
                data_transfer.test_transfer(table_name, model_cls)
