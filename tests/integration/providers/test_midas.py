import pytest
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text as sa_text

from opencdms.dtos.midas import source as midas_source_schema
from opencdms.models.midas import core as midas_models
from opencdms.provider.midas import MidasProvider
from opencdms.utils.db import get_midas_connection_string

DB_URL = get_midas_connection_string()
fake = Faker()
midas_provider = MidasProvider(models=midas_models)
db_engine = create_engine(DB_URL)

source_data = {
    'station_id': 1605,
    'src_name': 'BOTTOMS WOOD, ST HELENA',
    'high_prcn_lat': -15.9422,
    'high_prcn_lon': -5.6676,
    'loc_geog_area_id': 'SHEL',
    'src_bgn_date': '01-Jan-1958',
    'rec_st_ind': 1001,
    'src_type': 'SFC UA',
    'grid_ref_type': 'XX',
    'src_end_date': '31-Dec-3999',
    'elevation': 435,
    'wmo_region_code': 1,
    'zone_time': 0,
    'drainage_stream_id': '1866',
    'src_upd_date': '04-Nov-2019 16:03:40'
}


@pytest.fixture
def db_session():
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.close()


def setup_module(module):
    # Postgresql does not automatically reset ID
    # if a table is truncated like mysql does
    midas_models.Base.metadata.create_all(bind=db_engine)

    with db_engine.connect() as connection:
        with connection.begin():
            db_engine.execute(
                sa_text(
                    f'''
                    TRUNCATE TABLE {midas_models.Source.__tablename__}
                    RESTART IDENTITY CASCADE
                    '''
                ).execution_options(autocommit=True)
            )


def teardown_module(module):
    # Postgresql does not automatically reset ID
    # if a table is truncated like mysql does
    midas_models.Base.metadata.create_all(bind=db_engine)

    with db_engine.connect() as connection:
        with connection.begin():
            db_engine.execute(
                sa_text(
                    f'''TRUNCATE TABLE {midas_models.Source.__tablename__}
                     RESTART IDENTITY CASCADE'''
                ).execution_options(autocommit=True)
            )


@pytest.mark.order(2500)
def test_should_create_a_source(db_session):
    source = midas_provider.create(db_session, "Source", source_data)
    assert source.src_id == source_data['station_id']


@pytest.mark.order(2501)
def test_should_read_all_sources(db_session):
    sources = midas_provider.list(db_session, "Source")

    for source in sources:
        assert isinstance(source, midas_source_schema.Source)


@pytest.mark.order(2502)
def test_should_return_a_single_source(db_session):
    source = midas_provider.get(
        db_session,
        "Source",
        {"station_id": source_data["station_id"]}
    )

    assert source.src_id == source_data['station_id']


@pytest.mark.order(2503)
def test_should_update_source(db_session):
    updated_source = midas_provider.update(
        db_session, "Source",
        {"station_id": source_data["station_id"]},
        {
            "name": "Test station",
            "latitude": 67.111,
            "longitude": 128.454,
            "elevation": 45,
            "start_datetime": "2019-01-01",
            "end_datetime": "2056-12-31",
        }
    )

    assert updated_source.elevation == 45


@pytest.mark.order(2504)
def test_should_delete_source(db_session):
    deleted = midas_provider.delete(
        db_session,
        "Source",
        {"station_id": source_data["station_id"]}
    )

    assert deleted == {"station_id": source_data["station_id"]}
