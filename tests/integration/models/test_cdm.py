import pytest
from sqlalchemy import create_engine, schema
from sqlalchemy.orm import sessionmaker, close_all_sessions
from sqlalchemy.sql import text as sa_text
from opencdms.utils.db import get_cdm_connection_string
from opencdms.provider.opencdmsdb import mapper_registry, start_mappers
from opencdms.models import cdm
from datetime import datetime,timedelta

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
    feature1 = cdm.FeatureType( \
        name="Feature1", \
            description="A type of feature", \
                link="https://links.features.com/1"
            )
    db_session.add(feature1)
    db_session.commit()
    feature_types = db_session.query(cdm.FeatureType).all()
    assert type(feature1.id) is int
    assert len(feature_types) == 1


def test_should_create_observation_type(db_session):
    obs_type_1 = cdm.ObservationType( \
        name="Observation1", \
            description="A type of observation_type", \
                link="https://links.observation_types.com/1"
            )
    db_session.add(obs_type_1)
    db_session.commit()

    assert type(obs_type_1.id) is int
    obs_types = db_session.query(cdm.ObservationType).all()
    assert len(obs_types) == 1


def test_should_create_relationships(db_session):
    user = cdm.User(
        name="John Doe"
    )
    source = cdm.Source(
        name="Source 1",
        link="A link",
    )
    status = cdm.RecordStatus(
        name="ACCEPTED",
        description="Valid record"
        )
    observation = cdm.Observation(
        location=(2.323243434,4.24243434344234),
        version=1,
        change_date=datetime.utcnow(),
        comments="A simple observation",
        phenomenon_end=(datetime.utcnow()+ timedelta(days=1)),
        result_value=5.920399,
    )

    observation.record_status_ =status
    observation.user_ = user
    observation.source_ = source
    db_session.add(observation)
    db_session.commit()

    assert observation.record_status_ == status
    assert observation.user_ == user
    assert observation.source_ == source
    
