# utils/sqlite_to_postgres/data_transfer.py

import sqlite3
import psycopg
from dataclasses import astuple
from typing import Generator, List, Type
from datetime import datetime
from zoneinfo import ZoneInfo
from config.components.logging_config import logger
# from utils.sqlite_to_postgres.models import Genre, Person, FilmWork, GenreFilmWork, PersonFilmWork

class DataTransfer:
    """
    Class for transferring data from SQLite to PostgreSQL.
    """
    def __init__(self, sqlite_cursor: sqlite3.Cursor, postgres_cursor: psycopg.Cursor, postgres_conn: psycopg.Connection, batch_size: int = 100):
        self.sqlite_cursor = sqlite_cursor
        self.postgres_cursor = postgres_cursor
        self.postgres_conn = postgres_conn
        self.batch_size = batch_size

    def extract_data(self, table_name: str) -> Generator[List[sqlite3.Row], None, None]:
        """
        Extracts data from the table in SQLite.

        Args:
            table_name (str): Name of the table in the database.

        Yields:
            Generator[List[sqlite3.Row], None, None]: List of rows from the table.
        """
        self.sqlite_cursor.execute(f"SELECT * FROM {table_name}")
        while results := self.sqlite_cursor.fetchmany(self.batch_size):
            yield results

    def insert_data(self, table_name: str, data: List[Type]):
        """
        Inserts data into the table in PostgreSQL.

        Args:
            table_name (str): Name of the table in the database.
            data (List[Type]): List of instances of the dataclass.
        """
        if not data:
            return

        fields = data[0].__dict__.keys()
        values_placeholder = ", ".join(["%s"] * len(fields))
        query = f"INSERT INTO content.{table_name} ({', '.join(fields)}) VALUES ({values_placeholder}) " \
                f"ON CONFLICT (id) DO NOTHING"

        try:
            for i in range(0, len(data), self.batch_size):
                batch = data[i:i + self.batch_size]
                batch_as_tuples = [astuple(item) for item in batch]
                self.postgres_cursor.executemany(query, batch_as_tuples)
            self.postgres_conn.commit()
        except Exception as e:
            logger.error(f"Error inserting data into {table_name}: {e}")
            self.postgres_conn.rollback()

    def transform_data(self, table_name: str, model_cls: Type) -> Generator[List[Type], None, None]:
        """
        Iterates over the data extracted from SQLite and transforms it into instances of the dataclass.

        Args:
            table_name (str): Name of the table in the database.
            model_cls (Type): Class of the dataclass.

        Yields:
            Generator[List[Type], None, None]: List of instances of the dataclass.
        """
        for batch in self.extract_data(table_name):
            yield [
                model_cls(**{
                    key: (self.normalize_datetime(value) if key in ["created", "modified"] else value)
                    for key, value in self.map_fields(dict(model_item), model_cls).items()
                })
                for model_item in batch
            ]
                
    def map_fields(self, data: dict, model_cls: Type) -> dict:
        """
        Maps the fields from the extracted data to the fields of the dataclass.

        Args:
            data (dict): Extracted data from the database.
            model_cls (Type): Class of the dataclass.

        Returns:
            dict: Mapped fields.
        """
        field_mapping = getattr(model_cls, "field_mapping", {})
        return {field_mapping.get(key, key): value for key, value in data.items()}

    def truncate_table(self, table_name: str):
        """
        Truncates the table in PostgreSQL.

        Args:
            table_name (str): Name of the table in the database.
        """
        query = f"TRUNCATE TABLE content.{table_name} CASCADE"
        self.postgres_cursor.execute(query)

    def normalize_datetime(self, value: str) -> datetime:
        """
        Normalizes the datetime value to UTC.

        Args:
            value (str): Datetime value.

        Returns:
            datetime: Normalized datetime value.
        """
        if isinstance(value, str):
            # Parse the datetime string
            value = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if value.tzinfo is None:
            # Assume that the datetime is in UTC
            value = value.replace(tzinfo=ZoneInfo("UTC"))
        
        return value.astimezone(ZoneInfo("UTC"))

    def test_transfer(self, table_name: str, model_cls: Type):
        """
        Tests the data transfer by comparing the data in SQLite and PostgreSQL.

        Args:
            table_name (str): Name of the table in the database.
            model_cls (Type): Class of the dataclass.
        """
        self.sqlite_cursor.execute(f"SELECT * FROM {table_name}")
        while batch := self.sqlite_cursor.fetchmany(self.batch_size):
            original_data = [
                model_cls(**{
                    key: (self.normalize_datetime(value) if key in ["created", "modified"] else value)
                    for key, value in self.map_fields(dict(item), model_cls).items()
                })
                for item in batch
            ]
            ids = [item.id for item in original_data]

            self.postgres_cursor.execute(f"SELECT * FROM content.{table_name} WHERE id = ANY(%s)", [ids])
            transferred_data = [
                model_cls(**{
                    key: (self.normalize_datetime(value) if key in ["created", "modified"] else value)
                    for key, value in self.map_fields(item, model_cls).items()
                })
                for item in self.postgres_cursor.fetchall()
            ]

            for original, transferred in zip(original_data, transferred_data):
                if original != transferred:
                    print("Mismatch found:")
                    print(f"Original: {original}")
                    print(f"Transferred: {transferred}")

            assert len(original_data) == len(transferred_data), "Length mismatch"
            assert original_data == transferred_data, "Data mismatch"

    def transfer_table(self, table_name: str, model_cls: Type):
        """
        Transfers data from SQLite to PostgreSQL for the specified table.

        Args:
            table_name (str): Name of the table in the database.
            model_cls (Type): Class of the dataclass.
        """
        logger.info(f"Transferring data for table: {table_name}")

        self.truncate_table(table_name)

        for batch in self.transform_data(table_name, model_cls):
            self.insert_data(table_name, batch)
