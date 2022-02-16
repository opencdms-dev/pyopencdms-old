import datetime
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import func
from opencdms.models.climsoft.v4_1_1_core import (
    Observationfinal,
    Stationelement
)


def group_observation_final_data(
    db_session: Session,
    first_obs_date: bool = True
):
    obs_date = func.DATE(Observationfinal.obsDatetime).label("obsDate")
    subquery = db_session.query(
        Observationfinal.recordedFrom,
        Observationfinal.describedBy,
        obs_date
    ).subquery()

    return db_session.query(
        subquery.c.recordedFrom,
        subquery.c.describedBy,
        func.MIN(subquery.c.obsDate) if first_obs_date
        else func.MAX(subquery.c.obsDate)
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
    """
    Synchronizes stationelement with observationfinal using sqlalchemy
    api. Only updates/removes new/invalid rows
    """
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
    """
        Synchronizes stationelement with observationfinal using raw SQL.
        Truncates stationelement and then repopulates again.
    """
    db_session.execute(f"TRUNCATE {Stationelement.__tablename__}")
    db_session.commit()

    sql = f"""
    INSERT INTO {Stationelement.__tablename__}
    (recordedFrom, describedBy, beginDate)
    SELECT t.recordedFrom, t.describedBy, MIN(t.beginDate) as beginDate FROM(
        SELECT recordedFrom, describedBy, DATE(obsDatetime) as beginDate
        FROM {Observationfinal.__tablename__}
    ) t GROUP BY t.recordedFrom, t.describedBy
    """

    db_session.execute(sql)
    db_session.commit()


def auto_update_end_date(
    db_session: Session,
    delay_threshold: datetime.timedelta = None
):
    """
    Updates endDate column in stationelement if last observation data is
    older than delay_threshold
    """
    if delay_threshold is None:
        return

    obsfinal_grouped_data = group_observation_final_data(
        db_session=db_session,
        first_obs_date=False
    )

    for recordedFrom, describedBy, obsDate in obsfinal_grouped_data:
        if (datetime.datetime.utcnow().date() - obsDate) > delay_threshold:
            db_session.query(Stationelement).filter_by(
                recordedFrom=recordedFrom,
                describedBy=describedBy
            ).update({"endDate": obsDate})
            db_session.commit()
    return
