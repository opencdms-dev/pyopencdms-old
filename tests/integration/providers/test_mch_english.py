import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from opencdms.dtos.mch import station as mch_station_schema
from opencdms.models.mch import english as mch_english
from opencdms.provider.mch import MCHProvider
from opencdms.utils.db import get_mch_english_connection_string
from tests.unit.dtos.data import station_data

DB_URL = get_mch_english_connection_string()
db_engine = create_engine(DB_URL)

mch_provider = MCHProvider()


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


@pytest.mark.order(2400)
def test_should_create_a_station(db_session):
    station = mch_provider.create(db_session, "Station", station_data)
    assert station.Station == str(station_data['station_id'])


@pytest.mark.order(2401)
def test_should_read_all_stations(db_session):
    stations = mch_provider.list(db_session, "Station")

    for station in stations:
        assert isinstance(station, mch_station_schema.Station)


@pytest.mark.order(2402)
def test_should_return_a_single_station(db_session):
    station = mch_provider.get(
        db_session,
        "Station",
        {"station_id": station_data["station_id"]}
    )

    assert station.Station == str(station_data['station_id'])


@pytest.mark.order(2403)
def test_should_update_station(db_session):
    mch_provider.update(
        db_session,
        "Station",
        {"station_id": station_data["station_id"]},
        {'name': 'Updated Station Name'}
    )
    updated_station = mch_provider.get(
        db_session,
        "Station",
        {"station_id": station_data["station_id"]}
    )

    assert updated_station.StationName == 'Updated Station Name'


@pytest.mark.order(2404)
def test_should_delete_station(db_session):
    deleted = mch_provider.delete(
        db_session,
        "Station",
        {"station_id": station_data["station_id"]}
    )

    assert deleted["station_id"] == station_data["station_id"]
