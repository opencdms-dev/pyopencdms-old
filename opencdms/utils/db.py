from opencdms.config import config
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, Query


def get_connection_string(
    engine: str,
    driver: str,
    user: str,
    password: str,
    host: str,
    port: str,
    db_name: str,
) -> str:
    return f"{engine}+{driver}://{user}:{password}@{host}:{port}/{db_name}"


def get_clide_connection_string() -> str:
    return get_connection_string(
        engine=config.CLIDE_DB_ENGINE,
        driver=config.CLIDE_DB_DRIVER,
        user=config.CLIDE_DB_USER,
        password=config.CLIDE_DB_PASS,
        host=config.CLIDE_DB_HOST,
        port=config.CLIDE_DB_PORT,
        db_name=config.CLIDE_DB_NAME,
    )


def get_midas_pg_connection_string() -> str:
    return get_connection_string(
        engine=config.MIDAS_PG_DB_ENGINE,
        driver=config.MIDAS_PG_DB_DRIVER,
        user=config.MIDAS_PG_DB_USER,
        password=config.MIDAS_PG_DB_PASS,
        host=config.MIDAS_PG_DB_HOST,
        port=config.MIDAS_PG_DB_PORT,
        db_name=config.MIDAS_PG_DB_NAME,
    )


def get_climsoft_4_1_1_connection_string() -> str:
    return get_connection_string(
        engine=config.CLIMSOFT_DB_ENGINE,
        driver=config.CLIMSOFT_DB_DRIVER,
        user=config.CLIMSOFT_DB_USER,
        password=config.CLIMSOFT_DB_PASS,
        host=config.CLIMSOFT_DB_HOST,
        port=config.CLIMSOFT_DB_PORT,
        db_name=config.CLIMSOFT_DB_NAME,
    )


def get_mch_english_connection_string() -> str:
    return get_connection_string(
        engine=config.MCH_DB_ENGINE,
        driver=config.MCH_DB_DRIVER,
        user=config.MCH_DB_USER,
        password=config.MCH_DB_PASS,
        host=config.MCH_DB_HOST,
        port=config.MCH_DB_PORT,
        db_name=config.MCH_DB_NAME,
    )


def clide_session():
    DB_URL = get_clide_connection_string()
    db_engine = create_engine(DB_URL)
    SessionLocal = sessionmaker(bind=db_engine)
    session = SessionLocal()
    return session


def midas_pg_session():
    DB_URL = get_midas_pg_connection_string()
    db_engine = create_engine(DB_URL)
    SessionLocal = sessionmaker(bind=db_engine)
    session = SessionLocal()
    return session


def climsoft_session():
    DB_URL = get_climsoft_4_1_1_connection_string()
    db_engine = create_engine(DB_URL)
    SessionLocal = sessionmaker(bind=db_engine)
    session = SessionLocal()
    return session


def mch_session():
    DB_URL = get_mch_english_connection_string()
    db_engine = create_engine(DB_URL)
    SessionLocal = sessionmaker(bind=db_engine)
    session = SessionLocal()
    return session


def get_count(q: Query):
    """
    Return the number of rows that matches a query
    """
    count_q = q.statement.with_only_columns(
        func.count(), maintain_column_froms=True
    ).order_by(None)
    count = q.session.execute(count_q).scalar()
    return count
