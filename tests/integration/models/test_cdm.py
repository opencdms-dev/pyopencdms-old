import pytest
from sqlalchemy import create_engine, schema
from sqlalchemy.orm import sessionmaker, close_all_sessions
from sqlalchemy.sql import text as sa_text
from opencdms.utils.db import get_cdm_connection_string
from opencdms.provider.opencdmsdb import mapper_registry, start_mappers
from opencdms.models.cdm import Feature, FeatureType, RecordStatus


DB_URL = get_cdm_connection_string()
db_engine = create_engine(DB_URL)
Base = mapper_registry.generate_base()

@pytest.fixture
def db_session():
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.close()


def setup_module(module):
    schemas = {v.schema for k, v in Base.metadata.tables.items()}

    for _schema in schemas:
        if not db_engine.dialect.has_schema(db_engine, _schema):
            db_engine.execute(schema.CreateSchema(_schema))
    Base.metadata.create_all(bind=db_engine)
    start_mappers()


def teardown_module(module):
    close_all_sessions()
    Base.metadata.drop_all(bind=db_engine)

def test_create_feature(db_session):
    feature1 = FeatureType( \
        name="Feature1", \
            description="A type of feature", \
                link="https://links.features.com/1"
            )
    db_session.add(feature1)
    db_session.commit()

    assert type(feature1.id) is int

