import random
import uuid

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text as sa_text

from opencdms.models import clide
from opencdms.utils.db import get_clide_connection_string

DB_URL = get_clide_connection_string()


db_engine = create_engine(DB_URL)

station_status_data = dict(
    id=1,
    status="ACTIVE",
    description="test station status 1"
)

timezone_data = dict(
    id=1,
    tm_zone="UTC",
    utc_diff=0,
    description="UTC timezone"
)

station_data = dict(
    id=random.randint(11000, 22000),
    station_no=uuid.uuid4().hex[:15],
    status_id=station_status_data["id"],
    time_zone=timezone_data["tm_zone"],
    region='UK'
)


@pytest.fixture
def db_session():
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.close()


def setup_module(module):
    # Postgresql does not automatically reset ID
    # if a table is truncated like mysql does
    clide.Base.metadata.create_all(bind=db_engine)

    with db_engine.connect() as connection:
        with connection.begin():
            db_engine.execute(
                sa_text(
                    f'''TRUNCATE TABLE {clide.Station.__tablename__}
                     RESTART IDENTITY CASCADE'''
                ).execution_options(autocommit=True)
            )
            db_engine.execute(
                sa_text(
                    f'''TRUNCATE TABLE {clide.StationStatu.__tablename__}
                     RESTART IDENTITY CASCADE'''
                ).execution_options(autocommit=True)
            )
            db_engine.execute(
                sa_text(
                    f'''TRUNCATE TABLE {clide.StationTimezone.__tablename__}
                     RESTART IDENTITY CASCADE'''
                ).execution_options(autocommit=True)
            )

    Session = sessionmaker(bind=db_engine)
    session = Session()

    session.add(clide.StationStatu(**station_status_data))
    session.add(clide.StationTimezone(**timezone_data))

    session.commit()
    session.close()


def teardown_module(module):
    # Postgresql does not automatically reset ID
    # if a table is truncated like mysql does
    clide.Base.metadata.create_all(bind=db_engine)

    with db_engine.connect() as connection:
        with connection.begin():
            db_engine.execute(
                sa_text(
                    f'''TRUNCATE TABLE {clide.Station.__tablename__}
                    RESTART IDENTITY CASCADE'''
                ).execution_options(autocommit=True)
            )
            db_engine.execute(
                sa_text(
                    f'''TRUNCATE TABLE {clide.StationStatu.__tablename__}
                    RESTART IDENTITY CASCADE'''
                ).execution_options(autocommit=True)
            )
            db_engine.execute(
                sa_text(
                    f'''TRUNCATE TABLE {clide.StationTimezone.__tablename__}
                    RESTART IDENTITY CASCADE'''
                ).execution_options(autocommit=True)
            )


@pytest.mark.order(1100)
def test_should_create_a_station(db_session):
    station = clide.Station(**station_data)
    db_session.add(station)
    db_session.commit()

    assert station.id == station_data['id']


@pytest.mark.order(1101)
def test_should_read_all_stations(db_session):
    stations = db_session.query(clide.Station).all()

    for station in stations:
        assert isinstance(station, clide.Station)


@pytest.mark.order(1102)
def test_should_return_a_single_station(db_session):
    station = db_session.query(clide.Station).get(station_data['id'])

    assert station.id == station_data['id']


@pytest.mark.order(1103)
def test_should_update_station(db_session):
    db_session.query(clide.Station)\
        .filter_by(id=station_data['id']).update({'region': 'US'})
    db_session.commit()

    updated_station = db_session.query(clide.Station).get(station_data['id'])

    assert updated_station.region == 'US'


@pytest.mark.order(1104)
def test_should_delete_station(db_session):
    db_session.query(clide.Station).filter_by(id=station_data['id']).delete()
    db_session.commit()

    deleted_station = db_session.query(clide.Station).get(station_data['id'])

    assert deleted_station is None
