import random
import uuid

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.sql import text as sa_text

from opencdms.dtos.clide import station as clide_station_schema
from opencdms.models import clide
from opencdms.provider.clide import ClideProvider
from opencdms.utils.db import get_clide_connection_string

DB_URL = get_clide_connection_string()

db_engine = create_engine(DB_URL)
clide_provider = ClideProvider()

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
    station_id=random.randint(21000, 25000),
    station_no=uuid.uuid4().hex[:15],
    status_id=station_status_data["id"],
    timezone=timezone_data["tm_zone"],
    region='UK'
)


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

    SessionLocal = sessionmaker(bind=db_engine)
    session = SessionLocal()

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


@pytest.fixture
def db_session():
    SessionLocal = sessionmaker(bind=db_engine)
    session = SessionLocal()
    yield session
    session.close()


@pytest.mark.order(2100)
def test_should_create_a_station(db_session: Session):
    station = clide_provider.create(db_session, "Station", station_data)

    assert station.id == station_data['station_id']


@pytest.mark.order(2101)
def test_should_read_all_stations(db_session):
    stations = clide_provider.list(db_session, "Station")

    for station in stations:
        assert isinstance(station, clide_station_schema.Station)


@pytest.mark.order(2102)
def test_should_return_a_single_station(db_session):
    station = clide_provider.get(
        db_session,
        "Station",
        {"station_id": station_data['station_id']}
    )

    assert station.id == station_data['station_id']


@pytest.mark.order(2103)
def test_should_update_station(db_session):
    updated_station = clide_provider.update(
        db_session,
        "Station",
        {"station_id": station_data['station_id']},
        {
            'region': 'US',
            "station_no": station_data["station_no"],
            "timezone": station_data["timezone"],
            "status_id": station_data["status_id"]
        }
    )

    assert updated_station.region == 'US'


@pytest.mark.order(2104)
def test_should_delete_station(db_session):
    deleted = clide_provider.delete(
        db_session,
        "Station",
        {"station_id": station_data['station_id']}
    )

    assert deleted == {"station_id": station_data['station_id']}
