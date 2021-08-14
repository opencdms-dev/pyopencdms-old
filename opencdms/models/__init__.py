from typing import Callable, List, Optional, Sequence
from alembic import migration
from sqlalchemy import MetaData, create_engine
from alembic.autogenerate import compare_metadata


def filter_ignored_tables(
    tables: Sequence[str],
) -> Callable[[tuple], bool]:
    """ Accept sequence of table names to be ignored  when comparing model to\
         db schema
    Parameters
    -----
    `tables`: Sequence[str]
        Table names to be ignored

    Return
    ------
    `Callable[[tuple]], bool]`
    """

    def filter_func(item: tuple):
        """
        Return true if item's table name not in `tables`
        """
        operation: str = item[0]
        if operation == "add_table":
            _, table = item
            return table.name not in tables
        return True

    return filter_func


def get_schema_diff(
    metadata: MetaData,
    database_url: str,
    ignore_tables: Optional[Sequence[str]] = None,
) -> List[tuple]:
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
    List[tuple]

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
        diff = list(filter(filter_ignored_tables(ignore_tables), diff))
    return list(diff)


# TODO remove and use automated tests instead.
if __name__ == "__main__":
    from opencdms.models.clide import metadata, CLIDE_VIEWS

    print(
        get_schema_diff(
            metadata,
            "postgresql+psycopg2://localhost/clideDB",
            ignore_tables=CLIDE_VIEWS,
        )
    )
