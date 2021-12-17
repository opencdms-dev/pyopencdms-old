import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from opencdms.dtos.climsoft import station as climsoft_station_schema
from opencdms.models.climsoft import v4_1_1_core as climsoft
from opencdms.provider.climsoft import Climsoft4Provider
from opencdms.utils.db import get_climsoft_4_1_1_connection_string
from tests.unit.dtos.data import station_data

DB_URL = get_climsoft_4_1_1_connection_string()
db_engine = create_engine(DB_URL)
climsoft_provider = Climsoft4Provider()


@pytest.fixture
def db_session():
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.close()


def setup_module(module):
    climsoft.Base.metadata.create_all(db_engine)
    with db_engine.connect() as connection:
        trans = connection.begin()
        connection.execute('SET FOREIGN_KEY_CHECKS = 0;')
        for table in climsoft.metadata.sorted_tables:
            connection.execute(table.delete())
        connection.execute('SET FOREIGN_KEY_CHECKS = 1;')
        trans.commit()


def teardown_module(module):
    climsoft.Base.metadata.create_all(db_engine)
    with db_engine.connect() as connection:
        trans = connection.begin()
        connection.execute('SET FOREIGN_KEY_CHECKS = 0;')
        for table in climsoft.metadata.sorted_tables:
            connection.execute(table.delete())
        connection.execute('SET FOREIGN_KEY_CHECKS = 1;')
        trans.commit()


@pytest.mark.order(2200)
def test_should_create_a_station(db_session):
    station = climsoft_provider.create(db_session, "Station", station_data)
    assert station.stationId == str(station_data['station_id'])


@pytest.mark.order(2201)
def test_should_read_all_stations(db_session):
    stations = climsoft_provider.list(db_session, "Station")

    for station in stations:
        assert isinstance(station, climsoft_station_schema.Station)


@pytest.mark.order(2202)
def test_should_return_a_single_station(db_session):
    station = climsoft_provider.get(
        db_session,
        "Station",
        {"station_id": station_data["station_id"]}
    )

    assert station.stationId == str(station_data['station_id'])


@pytest.mark.order(2203)
def test_should_update_station(db_session):
    updated_station = climsoft_provider.update(
        db_session,
        "Station",
        {"station_id": station_data["station_id"]},
        {'country': 'US'}
    )

    assert updated_station.country == 'US'


@pytest.mark.order(2204)
def test_should_delete_station(db_session):
    deleted = climsoft_provider.delete(
        db_session,
        "Station",
        {"station_id": station_data["station_id"]}
    )

    assert deleted["station_id"] == station_data["station_id"]
