import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from opencdms.models.mch import english as mch_english
from opencdms.utils.db import get_mch_english_connection_string

DB_URL = get_mch_english_connection_string()

db_engine = create_engine(DB_URL)

station_data = dict(
    Station='TEST',
    StationName='Test Station'
)


@pytest.fixture
def db_session():
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.close()


def setup_module(module):
    mch_english.Base.metadata.create_all(db_engine)
    with db_engine.connect() as connection:
        trans = connection.begin()
        connection.execute('SET FOREIGN_KEY_CHECKS = 0;')
        for table in mch_english.metadata.sorted_tables:
            connection.execute(table.delete())
        connection.execute('SET FOREIGN_KEY_CHECKS = 1;')
        trans.commit()


def teardown_module(module):
    mch_english.Base.metadata.create_all(db_engine)
    with db_engine.connect() as connection:
        trans = connection.begin()
        connection.execute('SET FOREIGN_KEY_CHECKS = 0;')
        for table in mch_english.metadata.sorted_tables:
            connection.execute(table.delete())
        connection.execute('SET FOREIGN_KEY_CHECKS = 1;')
        trans.commit()


@pytest.mark.order(1400)
def test_should_create_a_station(db_session):
    station = mch_english.Station(**station_data)
    db_session.add(station)
    db_session.commit()

    assert station.Station == station_data['Station']


@pytest.mark.order(1401)
def test_should_read_all_stations(db_session):
    stations = db_session.query(mch_english.Station).all()

    for station in stations:
        assert isinstance(station, mch_english.Station)


@pytest.mark.order(1402)
def test_should_return_a_single_station(db_session):
    station = db_session.query(mch_english.Station)\
        .get(station_data['Station'])

    assert station.Station == station_data['Station']


@pytest.mark.order(1403)
def test_should_update_station(db_session):
    db_session.query(mch_english.Station)\
        .filter_by(Station=station_data['Station'])\
        .update({'StationName': 'Updated Station Name'})
    db_session.commit()

    updated_station = db_session.query(mch_english.Station)\
        .get(station_data['Station'])

    assert updated_station.StationName == 'Updated Station Name'


@pytest.mark.order(1404)
def test_should_delete_station(db_session):
    db_session.query(mch_english.Station)\
        .filter_by(Station=station_data['Station']).delete()
    db_session.commit()

    deleted_station = db_session.query(mch_english.Station)\
        .get(station_data['Station'])

    assert deleted_station is None
