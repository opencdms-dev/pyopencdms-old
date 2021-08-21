import pytest
from sqlalchemy import Column, Integer, String, create_engine, inspect
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import MetaData
from opencdms.models import get_schema_diff


TABLE_NAME = "samples"


def get_column_names(db_engine, tablename):
    inspector = inspect(db_engine)
    table_columns = inspector.get_columns(tablename)
    return [x["name"] for x in table_columns]


@pytest.fixture
def db_url() -> str:
    return "sqlite:///test.db"


@pytest.fixture
def db_engine(db_url: str) -> Engine:
    return create_engine(db_url)


@pytest.fixture
def metadata(db_engine) -> MetaData:
    return MetaData(db_engine)


@pytest.fixture
def Base(metadata):
    return declarative_base(metadata=metadata)


@pytest.fixture
def db(Base, metadata: MetaData, db_engine: Engine):
    class Sample(Base):
        __tablename__ = TABLE_NAME
        id = Column(Integer, primary_key=True)
        key = Column(String)
        value = Column(Integer)

    inspector = inspect(db_engine)
    assert not inspector.has_table(TABLE_NAME)
    metadata.create_all()
    assert inspector.has_table(TABLE_NAME)
    yield
    metadata.drop_all()
    assert not inspector.has_table(TABLE_NAME)


def test_schema_diff(db, metadata: MetaData, db_engine: Engine, db_url: str):
    assert "new" not in get_column_names(db_engine, TABLE_NAME)
    schema_diff = get_schema_diff(metadata, db_url)
    assert len(schema_diff) == 0
    db_engine.execute(f"ALTER TABLE {TABLE_NAME} ADD COLUMN new integer")
    assert "new" in get_column_names(db_engine, TABLE_NAME)
    schema_diff = get_schema_diff(metadata, db_url)
    assert len(schema_diff) == 1
