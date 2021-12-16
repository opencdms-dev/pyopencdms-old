from opencdms.provider.opencdms import OpenCDMSProvider, ProviderConfig
from tests.unit.dtos.data import station_data
from opencdms.models import clide
from opencdms.models.mch import english as mch
from opencdms.utils.db import get_clide_connection_string, \
    get_mch_english_connection_string
from sqlalchemy import create_engine
from sqlalchemy.sql import text as sa_text
from sqlalchemy.orm import sessionmaker

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

    SessionLocal = sessionmaker(bind=db_engine)
    session = SessionLocal()
    station_status = clide.StationStatu(**station_status_data)
    session.add(station_status)
    timezone = clide.StationTimezone(**timezone_data)
    session.add(timezone)

    session.commit()

    provider = OpenCDMSProvider(ProviderConfig(enable_clide=True))

    station_data["timezone"] = timezone.id
    station_data["status_id"] = station_status.id

    session.close()

    station = provider.create("Station", station_data)
    assert isinstance(station["clide"], clide.Station)

    station = provider.get("Station", {"id": station_data["station_id"]})
    assert isinstance(station["clide"], clide.Station)

    stations = provider.list("Station")
    for station in stations["clide"]:
        assert isinstance(station, clide.Station)

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
    assert isinstance(station["mch"], mch.Station)

    station = provider.get("Station", {"Station": station_data["station_id"]})
    assert isinstance(station["mch"], mch.Station)

    stations = provider.list("Station")
    for station in stations["mch"]:
        assert isinstance(station, mch.Station)

    station = provider.update(
        "Station",
        {"Station": station_data["station_id"]},
        {'name': 'Updated Name'}
    )
    print(station["mch"].StationName)
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
