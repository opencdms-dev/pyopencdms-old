import pytest
from sqlalchemy import create_engine, schema
from sqlalchemy.orm import sessionmaker, close_all_sessions
from sqlalchemy.sql import text as sa_text
from opencdms.utils.db import get_cdm_connection_string
from opencdms.provider.opencdmsdb import mapper_registry, start_mappers
from opencdms.models import cdm
from datetime import datetime,timedelta
from uuid import uuid4

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
    feature_type = cdm.FeatureType( \
        name="Feature1", \
            description="A type of feature", \
                link="https://links.features.com/1"
            )
    user = cdm.User(
        name="John Doe"
    )
    status = cdm.RecordStatus(
        name="ACCEPTED",
        description="Valid record"
        )
    db_session.add(feature_type)
    db_session.add(user)
    db_session.add(status)
    db_session.commit()


    feature = cdm.Feature(
        id=str(uuid4()),
        type_id=feature_type.id,
        elevation=2.9,
        name="FEATURE2",
        geometry="POINT(-71.060316 48.432044)",
        description="A description"
    )
    collection = cdm.Collection(
        id=str(uuid4()),
        name="Collection 1",
        link=" A link"
    )
    observer = cdm.Observer(
        id=str(uuid4()),
        description="A good observer",
        link="A link",
        location="POINT(-71.060316 48.432044)"
    )
    host = cdm.Host(
        id=str(uuid4()),
        name="Host Zone",
        version=1,
        change_date=datetime.utcnow(),
        user_id=user.id,
        comments="A comment",
        status_id=status.id
    )
    db_session.add(host)
    db_session.add(feature)
    db_session.add(collection)
    db_session.add(observer)
    db_session.commit()

    

    user = cdm.User(
        name="John Doe"
    )
    source = cdm.Source(
        name="Source 1",
        link="A link",
    )

    observation_id = str(uuid4())
    observation = cdm.Observation(
        id=observation_id,
        location="POINT(-71.060316 48.432044)",
        version=1,
        change_date=datetime.utcnow(),
        comments="A simple observation",
        phenomenon_end=(datetime.utcnow()+ timedelta(days=1)),
        result_value=5.920399,
        feature_of_interest_id=feature.id,
        collection_id=collection.id,
        elevation=5.9,
        observer_id=observer.id,
        host_id=host.id

    )

    observation.record_status_ =status
    observation.user_ = user
    observation.source_ = source
    db_session.add(observation)
    db_session.commit()

    observation = db_session.query(cdm.Observation).filter(cdm.Observation.id == observation_id).one()
    assert observation.record_status_ == status
    assert observation.user_ == user
    assert observation.source_ == source
    
