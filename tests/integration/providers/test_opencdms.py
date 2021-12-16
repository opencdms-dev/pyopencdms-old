from opencdms.provider.opencdms import OpenCDMSProvider, ProviderConfig
from tests.unit.dtos.data import station_data
from opencdms.models import clide
from opencdms.models.mch import english as mch
from opencdms.utils.db import get_clide_connection_string, \
    get_mch_english_connection_string
from sqlalchemy import create_engine
from sqlalchemy.sql import text as sa_text
from sqlalchemy.orm import sessionmaker
from opencdms.dtos.clide import station as clide_station
from opencdms.dtos.clide import stationstatu as clide_station_status
from opencdms.dtos.clide import stationtimezone as clide_station_timezone
from opencdms.dtos.mch import station as mch_station

timezone_data = dict(
    id=1,
    tm_zone="UTC",
    utc_diff=0,
    description="UTC timezone"
)

station_status_data = dict(
    id=1,
    status="ACTIVE",
    description="test station status 1"
)


def test_clide_provider():
    DB_URL = get_clide_connection_string()
    db_engine = create_engine(DB_URL)

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

    provider = OpenCDMSProvider(ProviderConfig(enable_clide=True))

    station_status = provider.create("StationStatu", station_status_data)
    assert isinstance(station_status["clide"], clide_station_status.StationStatu)

    timezone = provider.create("StationTimezone", timezone_data)
    assert isinstance(timezone["clide"], clide_station_timezone.StationTimezone)

    station_data["timezone"] = timezone["clide"].tm_zone
    station_data["status_id"] = station_status["clide"].id

    station = provider.create("Station", station_data)
    assert isinstance(station["clide"], clide_station.Station)

    station = provider.get("Station", {"id": station_data["station_id"]})
    assert isinstance(station["clide"], clide_station.Station)

    stations = provider.list("Station")
    for station in stations["clide"]:
        print(station)
        assert isinstance(station, clide_station.Station)
    print(station_data["station_id"])
    station = provider.update(
        "Station",
        {"id": station_data["station_id"]},
        {'region': 'US'}
    )

    assert station["clide"].region == 'US'

    deleted = provider.delete(
        "Station",
        {"id": station_data['station_id']}
    )

    assert deleted["clide"] == {"id": station_data['station_id']}


def test_mch_provider():
    DB_URL = get_mch_english_connection_string()
    db_engine = create_engine(DB_URL)

    mch.Base.metadata.create_all(db_engine)
    with db_engine.connect() as connection:
        trans = connection.begin()
        connection.execute('SET FOREIGN_KEY_CHECKS = 0;')
        for table in mch.metadata.sorted_tables:
            connection.execute(table.delete())
        connection.execute('SET FOREIGN_KEY_CHECKS = 1;')
        trans.commit()

    provider = OpenCDMSProvider(ProviderConfig(enable_mch=True))

    station = provider.create("Station", station_data)
    assert isinstance(station["mch"], mch_station.Station)

    station = provider.get("Station", {"Station": station_data["station_id"]})
    assert isinstance(station["mch"], mch_station.Station)

    stations = provider.list("Station")
    for station in stations["mch"]:
        assert isinstance(station, mch_station.Station)

    station = provider.update(
        "Station",
        {"Station": station_data["station_id"]},
        {'name': 'Updated Name'}
    )

    assert station["mch"].StationName == 'Updated Name'

    deleted = provider.delete(
        "Station",
        {"Station": station_data['station_id']}
    )

    assert deleted["mch"] == {"Station": station_data['station_id']}

    mch.Base.metadata.create_all(db_engine)
    with db_engine.connect() as connection:
        trans = connection.begin()
        connection.execute('SET FOREIGN_KEY_CHECKS = 0;')
        for table in mch.metadata.sorted_tables:
            connection.execute(table.delete())
        connection.execute('SET FOREIGN_KEY_CHECKS = 1;')
        trans.commit()
