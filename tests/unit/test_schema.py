import pytest
from sqlalchemy import Column, Integer, String, create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base

from opencdms.models import get_schema_diff

DB_URL = "sqlite:///test.db"
TABLE_NAME = "samples"

db_engine = create_engine(DB_URL)
base = declarative_base()


def get_column_names(engine, tablename):
    inspector = inspect(engine)
    table_columns = inspector.get_columns(tablename)
    return [x["name"] for x in table_columns]


def setup_module(module):
    base.metadata.drop_all(db_engine)


def teardown_module(module):
    base.metadata.drop_all(db_engine)


@pytest.mark.order(1)
def test_inspector_should_not_find_table():
    inspector = inspect(db_engine)
    assert not inspector.has_table(TABLE_NAME)


@pytest.mark.order(2)
def test_should_create_table_and_inspector_should_find_table():
    class Sample(base):
        __tablename__ = TABLE_NAME
        id = Column(Integer, primary_key=True)
        key = Column(String)
        value = Column(Integer)

    base.metadata.create_all(db_engine)

    inspector = inspect(db_engine)
    assert inspector.has_table(TABLE_NAME)


@pytest.mark.order(3)
def test_schema_diff_should_be_zero():
    schema_diff = get_schema_diff(base.metadata, DB_URL)
    assert len(schema_diff) == 0


@pytest.mark.order(4)
def test_schema_diff_should_be_one():
    db_engine.execute(f"ALTER TABLE {TABLE_NAME} ADD COLUMN new integer")
    assert "new" in get_column_names(db_engine, TABLE_NAME)
    schema_diff = get_schema_diff(base.metadata, DB_URL)
    assert len(schema_diff) == 1
