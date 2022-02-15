from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import func
from sqlalchemy.sql import select, insert
from opencdms.models.climsoft.v4_1_1_core import Observationfinal, Stationelement


def sync_stationelement_with_observationfinal_sqla(db_session: Session):
    select_stmt = select(
        Observationfinal.recordedFrom,
        Observationfinal.describedBy,
        func.DATE(Observationfinal.obsDatetime).label("beginDate")
    ).group_by(
        Observationfinal.recordedFrom,
        Observationfinal.describedBy
    ).order_by(
        "beginDate"
    )
    insert_stmt = insert(
        Stationelement
    ).from_select(
        ["recordedFrom", "describedBy", "beginDate"], select_stmt
    ).prefix_with("IGNORE")

    db_session.execute(insert_stmt)
    db_session.commit()


def sync_stationelement_with_observationfinal_sql(db_session: Session):
    sql = f"""
    INSERT IGNORE INTO {Stationelement.__tablename__} (recordedFrom, describedBy, beginDate)
        SELECT recordedFrom, describedBy, DATE(obsDatetime) as beginDate
        FROM {Observationfinal.__tablename__}
        GROUP BY recordedFrom, describedBy
        ORDER BY beginDate;
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


