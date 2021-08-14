from typing import Callable, Optional, Sequence, Tuple
from alembic import migration
from sqlalchemy import Table, MetaData
from alembic.autogenerate import compare_metadata
from sqlalchemy import create_engine
from logging import getLogger


logger = getLogger(__name__)


class DatabaseModelMismatchError(Exception):
    pass


def filter_ignored_tables(
    tables: Sequence[str],
) -> Callable[[Tuple[str, Table]], bool]:
    """ Accept sequence of table names to be ignored  when comparing model to\
         db schema
    Parameters
    -----
    `tables`: Sequence[str]
        Table names to be ignored

    Return
    ------
    `Callable[[Tuple[str, Table]], bool]`
    """

    def filter_func(item: Tuple[str, Table]):
        """
        Return true if item's table name not in `tables`
        """
        _, table = item
        return table.name not in tables

    return filter_func


def check_schema(
    metadata: MetaData,
    database_url: str,
    ignore_tables: Optional[Sequence[str]] = None,
):
    """
    Parameters
    -----
    `metadata`: Metadata
        Sqlalchemy Metadata
    `database_url`:
        Target databse url e.g. `sqlite://`
    `ignore_tables`: Sequence[str] | None
        List of table names to be ignored

    Return
    ------
    `None`

    Raises
    ------
    `DatabaseModelMismatchError`:
        if there is mismatch between models in metadata and target\
        database schema
    """
    engine = create_engine(database_url)
    mc = migration.MigrationContext.configure(engine.connect())
    diff = compare_metadata(mc, metadata)
    if ignore_tables is not None:
        diff = filter(filter_ignored_tables(ignore_tables), diff)
    if len(list(diff)) != 0:
        raise DatabaseModelMismatchError(
            "Database schema does not match model definitions"
        )
    print("\n\nModel definition matches database schema\n\n")


if __name__ == "__main__":
    from opencdms.models.clide import metadata, CLIDE_VIEWS

    check_schema(
        metadata,
        "postgresql+psycopg2://localhost/clideDB",
        ignore_tables=CLIDE_VIEWS,
    )
