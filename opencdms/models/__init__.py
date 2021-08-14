from typing import Optional, Sequence, Tuple
from alembic import migration
from sqlalchemy import Table
from alembic.autogenerate import compare_metadata
from sqlalchemy import create_engine
from opencdms.models.clide import metadata, CLIDE_VIEWS
from logging import getLogger


logger = getLogger(__name__)


def filter_ignored_tables(tables: Sequence[str]):
    def filter_func(item: Tuple[str, Table]):
        _, table = item
        return table.name not in tables

    return filter_func


def check_schema(database_url: str, ignore_tables: Optional[Sequence[str]] = None):
    engine = create_engine(database_url)
    mc = migration.MigrationContext.configure(engine.connect())
    diff = compare_metadata(mc, metadata)
    if ignore_tables is not None:
        diff = filter(filter_ignored_tables(ignore_tables), diff)
    if len(list(diff)) != 0:
        raise Exception("Database schema does not match model definitions")
    print("Model definition matches database schema")


if __name__ == "__main__":
    check_schema("postgresql+psycopg2://localhost/clideDB", ignore_tables=CLIDE_VIEWS)
