import datetime
import uuid
import random
import pytest
from sqlalchemy import create_engine
from sqlalchemy.sql import text as sa_text
from sqlalchemy.orm import sessionmaker
from opencdms.models.midas import core as midas_models
from test_util import get_midas_connection_string
from faker import Faker

DB_URL = get_midas_connection_string()
fake = Faker()

db_engine = create_engine(DB_URL)

source_data = {'src_id': 1605, 'src_name': 'BOTTOMS WOOD, ST HELENA', 'high_prcn_lat': -15.9422, 'high_prcn_lon': -5.6676, 'loc_geog_area_id': 'SHEL', 'src_bgn_date': '01-Jan-1958', 'rec_st_ind': 1001, 'src_type': 'SFC UA', 'grid_ref_type': 'XX', 'src_end_date': '31-Dec-3999', 'elevation': 435, 'wmo_region_code': 1, 'zone_time': 0, 'drainage_stream_id': 1866.0, 'src_upd_date': '04-Nov-2019 16:03:40'}


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

    Session = sessionmaker(bind=db_engine)
    session = Session()

    session.add(midas_models.Source(**source_data))

    session.commit()
    session.close()


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


@pytest.mark.order(500)
def test_should_create_a_source(db_session):
    source = midas_models.Source(**source_data)
    db_session.add(source)
    db_session.commit()

    assert source.source_id == source_data['source_id']


@pytest.mark.order(501)
def test_should_read_all_sources(db_session):
    sources = db_session.query(midas_models.Source).all()

    for source in sources:
        assert isinstance(source, midas_models.Source)


@pytest.mark.order(502)
def test_should_return_a_single_source(db_session):
    source = db_session.query(midas_models.Source) \
        .get(source_data['source_id'])

    assert source.source_id == source_data['source_id']


@pytest.mark.order(503)
def test_should_update_source(db_session):
    db_session.query(midas_models.Source) \
        .filter_by(source_id=source_data['source_id']) \
        .update({'region': 'US'})
    db_session.commit()

    updated_source = db_session.query(midas_models.Source) \
        .get(source_data['source_id'])

    assert updated_source.region == 'US'


@pytest.mark.order(504)
def test_should_delete_source(db_session):
    db_session.query(midas_models.Source) \
        .filter_by(source_id=source_data['source_id']).delete()
    db_session.commit()

    deleted_source = db_session.query(midas_models.Source) \
        .get(source_data['source_id'])

    assert deleted_source is None
