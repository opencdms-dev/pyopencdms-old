from pprint import pprint
from typing import Callable, List, Optional, Sequence
from alembic import migration
from sqlalchemy import MetaData, create_engine, Table, Index
from alembic.autogenerate import compare_metadata


def filter_out_excluded_tables(
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
        target_object = item[1]
        if isinstance(target_object, Table):
            return target_object.name not in tables
        if isinstance(target_object, Index):
            return target_object.table.name not in tables
        return True

    return filter_func


def filter_in_included_tables(
    tables: Sequence[str],
) -> Callable[[tuple], bool]:
    """ Accept sequence of table names to be included  when comparing model to\
         db schema
    Parameters
    -----
    `tables`: Sequence[str]
        Table names to be included, other tables not in this list would be ignored.

    Return
    ------
    `Callable[[tuple]], bool]`
    """

    def filter_func(item: tuple):
        """
        Return true if item's table name not in `tables`
        """
        target_object = item[1]
        if isinstance(target_object, Table):
            return target_object.name in tables
        if isinstance(target_object, Index):
            return target_object.table.name in tables
        return True

    return filter_func


def get_schema_diff(
    metadata: MetaData,
    database_url: str,
    include_tables: Optional[Sequence[str]] = None,
    exclude_tables: Optional[Sequence[str]] = None,
) -> List[tuple]:
    """
    Parameters
    -----
    `metadata`: Metadata
        Sqlalchemy Metadata
    `database_url`:
        Target databse url e.g. `sqlite://`
    `include_tables`: Sequence[str] | None
        List of table names to check against the database
    `exclude_tables`: Sequence[str] | None
        List of table names to be ignored

    Return
    ------
    List[tuple]

    """
    engine = create_engine(database_url)
    mc = migration.MigrationContext.configure(engine.connect())
    diff = compare_metadata(mc, metadata)
    if include_tables is not None and exclude_tables is not None:
        raise Exception("`include_tables` and `exclude_tables` must not be used together") #TODO define custom error class
    if exclude_tables is not None:
        diff = list(filter(filter_out_excluded_tables(exclude_tables), diff))
    if include_tables is not None:
        diff = list(filter(filter_in_included_tables(include_tables), diff))
    return list(diff)

