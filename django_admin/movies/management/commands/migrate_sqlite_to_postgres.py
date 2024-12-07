# movies/management/commands/migrate_sqlite_to_postgres.py

from django.core.management.base import BaseCommand
from utils.sqlite_to_postgres.run import run_migration
from django.conf import settings
from types import MappingProxyType
from pathlib import Path
from config.components.logging_config import logger

class Command(BaseCommand):
    """
    Django management command to migrate data from a SQLite database 
    to a PostgreSQL database.

    Usage:
        python manage.py migrate_sqlite_to_postgres

    Steps:
        1. Get the SQLite database path.
        2. Get PostgreSQL connection settings.
        3. Run the migration function.
    """
    help = "Migrate data from SQLite to PostgreSQL"

    def handle(self, *args, **options):
        logger.info("Migration started.")
        try:
            # Get the SQLite database path
            sqlite_db_path = self.get_sqlite_path()
            logger.info(f"SQLite database path: {sqlite_db_path}")

            # Get PostgreSQL connection settings
            dls_postgres = self.get_postgres_dls()
            logger.info(f"PostgreSQL connection settings: {dls_postgres}")

            # Run the migration function
            run_migration(sqlite_db_path, dls_postgres)
            logger.info("Migration completed successfully.")
        except Exception as e:
            logger.error(f"Migration failed: {e}")
            raise e
    
    def get_postgres_dls(self) -> dict:
        """
        Fetch and transform PostgreSQL connection settings from Django settings.

        Removes unsupported options and validates that the database engine is PostgreSQL.

        Returns:
            dict: A dictionary of PostgreSQL connection settings.
        """
        dls = settings.DATABASES['default'].copy()

        if dls.get('ENGINE') != 'django.db.backends.postgresql':
            raise ValueError("The default database is not configured for PostgreSQL.")

        transformed_dls = {
            'dbname': dls.get('NAME'),
            'user': dls.get('USER'),
            'password': dls.get('PASSWORD'),
            'host': dls.get('HOST'),
            'port': dls.get('PORT'),
        }

        # Handle additional options, if any
        options = dls.get('OPTIONS', {}).get('options')
        if options:
            transformed_dls['options'] = options

        return MappingProxyType(transformed_dls)

    
    def get_sqlite_path(self) -> str:
        """
        Fetch the path to the SQLite database.

        Returns:
            str: The absolute path to the SQLite database file.
        Raises:
            FileNotFoundError: If the SQLite database file does not exist.
        """
        sqlite_path = settings.BASE_DIR / "data" / "db" / "db.sqlite"

        # Convert to an absolute path
        sqlite_path = Path(sqlite_path).resolve()

        # Check if the file exists
        if not sqlite_path.is_file():
            raise FileNotFoundError(f"The SQLite database file does not exist: {sqlite_path}")

        return str(sqlite_path)