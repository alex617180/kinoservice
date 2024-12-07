# utils/sqlite_to_postgres/models.py

from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID
from datetime import datetime, date
from zoneinfo import ZoneInfo

@dataclass
class Genre:
    id: UUID
    name: str
    description: Optional[str] = None
    created: datetime = field(default_factory=lambda: datetime.now(ZoneInfo("UTC")))
    modified: datetime = field(default_factory=lambda: datetime.now(ZoneInfo("UTC")))
    field_mapping = {
        "created_at": "created",
        "updated_at": "modified",
    }

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = UUID(self.id)

@dataclass
class Person:
    id: UUID
    full_name: str
    gender: Optional[str] = None
    created: datetime = field(default_factory=lambda: datetime.now(ZoneInfo("UTC")))
    modified: datetime = field(default_factory=lambda: datetime.now(ZoneInfo("UTC")))

    field_mapping = {
        "created_at": "created",
        "updated_at": "modified",
    }

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = UUID(self.id)

@dataclass
class FilmWork:
    id: UUID
    title: str
    type: str
    description: Optional[str] = None
    creation_date: Optional[date] = None
    rating: Optional[float] = None
    file_path: Optional[str] = None
    created: datetime = field(default_factory=lambda: datetime.now(ZoneInfo("UTC")))
    modified: datetime = field(default_factory=lambda: datetime.now(ZoneInfo("UTC")))

    field_mapping = {
        "created_at": "created",
        "updated_at": "modified",
    }

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = UUID(self.id)

@dataclass
class GenreFilmWork:
    id: UUID
    genre_id: UUID
    film_work_id: UUID
    created: datetime = field(default_factory=lambda: datetime.now(ZoneInfo("UTC")))

    field_mapping = {
        "created_at": "created",
    }

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = UUID(self.id)
        if isinstance(self.genre_id, str):
            self.genre_id = UUID(self.genre_id)
        if isinstance(self.film_work_id, str):
            self.film_work_id = UUID(self.film_work_id)

@dataclass
class PersonFilmWork:
    id: UUID
    person_id: UUID
    film_work_id: UUID
    role: str
    created: datetime = field(default_factory=lambda: datetime.now(ZoneInfo("UTC")))

    field_mapping = {
        "created_at": "created",
    }

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = UUID(self.id)
        if isinstance(self.person_id, str):
            self.person_id = UUID(self.person_id)
        if isinstance(self.film_work_id, str):
            self.film_work_id = UUID(self.film_work_id)
