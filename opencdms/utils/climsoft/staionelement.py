from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import func
from opencdms.models.climsoft.v4_1_1_core import (
    Observationfinal,
    Stationelement
)


def group_observation_final_data(db_session: Session):
    subquery = db_session.query(
        Observationfinal.recordedFrom,
        Observationfinal.describedBy,
        func.DATE(Observationfinal.obsDatetime).label("beginDate")
    ).order_by(
        "beginDate"
    ).subquery()

    return db_session.query(
        subquery
    ).group_by(
        "recordedFrom",
        "describedBy"
    ).all()


def get_station_element_data(db_session: Session):
    return db_session.query(
        Stationelement.recordedFrom,
        Stationelement.describedBy,
        Stationelement.beginDate
    ).order_by(Stationelement.beginDate).all()


def sync_stationelement_with_observationfinal_sqla(db_session: Session):
    observationfinal_grouped_rows = group_observation_final_data(
        db_session
    )
    station_element_rows = get_station_element_data(
        db_session
    )

    obsfinal_set = {
        "#-#".join([str(row[0]), str(row[1]), str(row[2])])
        for row in observationfinal_grouped_rows
    }

    stelement_set = {
        "#-#".join([str(row[0]), str(row[1]), str(row[2])])
        for row in station_element_rows
    }

    to_insert_set = obsfinal_set - stelement_set
    to_delete_set = stelement_set - obsfinal_set

    for item in to_insert_set:
        recordedFrom, describedBy, beginDate = item.split("#-#")
        db_session.add(Stationelement(
            recordedFrom=recordedFrom,
            describedBy=int(describedBy),
            beginDate=beginDate
        ))
    db_session.commit()

    for item in to_delete_set:
        recordedFrom, describedBy, beginDate = item.split("#-#")
        db_session.query(
            Stationelement
        ).filter_by(
            recordedFrom=recordedFrom,
            describedBy=int(describedBy),
            beginDate=beginDate
        ).delete()
        db_session.commit()


def sync_stationelement_with_observationfinal_sql(db_session: Session):
    db_session.execute(f"TRUNCATE {Stationelement.__tablename__}")
    db_session.commit()

    sql = f"""
    INSERT INTO {Stationelement.__tablename__}
    (recordedFrom, describedBy, beginDate)
    SELECT * FROM(
        SELECT recordedFrom, describedBy, DATE(obsDatetime) as beginDate
        FROM {Observationfinal.__tablename__}
        ORDER BY beginDate ASC
    ) t GROUP BY t.recordedFrom, t.describedBy
    """

    db_session.execute(sql)
    db_session.commit()


if __name__ == "__main__":
    from opencdms.utils.db import get_connection_string
    from sqlalchemy.engine import create_engine
    from sqlalchemy.orm.session import sessionmaker
    DB_URL = get_connection_string(
        "mysql",
        "mysqldb",
        "root",
        "password",
        "127.0.0.1",
        "23306",
        "mariadb_climsoft_test_db_v4"
    )
    db_engine = create_engine(DB_URL)
    SessionLocal = sessionmaker(bind=db_engine)
    session = SessionLocal()
    sync_stationelement_with_observationfinal_sql(session)
    sync_stationelement_with_observationfinal_sqla(session)
    session.close()
