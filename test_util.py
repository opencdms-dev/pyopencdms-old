import os

from dotenv import load_dotenv

load_dotenv()


def get_connection_string(
    engine: str,
    driver: str,
    user: str,
    password: str,
    host: str,
    port: str,
    db_name: str
) -> str:
    return f"{engine}+{driver}://{user}:{password}@{host}:{port}/{db_name}"


def get_clide_connection_string() -> str:
    return get_connection_string(
        engine="postgresql",
        driver="psycopg2",
        user=os.getenv("CLIDE_DB_USER", "postgres"),
        password=os.getenv("CLIDE_DB_PASSWORD", "password"),
        host=os.getenv("CLIDE_DB_HOST", "api.opencdms.org"),
        port=os.getenv("CLIDE_DB_PORT", 5432),
        db_name=os.getenv("CLIDE_DB_NAME", "postgres")
    )


def get_midas_connection_string() -> str:
    return get_connection_string(
        engine="postgresql",
        driver="psycopg2",
        user=os.getenv("MIDAS_DB_USER", "postgres"),
        password=os.getenv("MIDAS_DB_PASSWORD", "password"),
        host=os.getenv("MIDAS_DB_HOST", "api.opencdms.org"),
        port=os.getenv("MIDAS_DB_PORT", 5432),
        db_name=os.getenv("MIDAS_DB_NAME", "postgres")
    )


def get_climsoft_4_1_1_connection_string() -> str:
    return get_connection_string(
        engine="mysql",
        driver="mysqldb",
        user=os.getenv("CLIMSOFT_DB_USER", "root"),
        password=os.getenv("CLIMSOFT_DB_PASSWORD", "password"),
        host=os.getenv("CLIMSOFT_DB_HOST", "api.opencdms.org"),
        port=os.getenv("CLIMSOFT_DB_PORT", 3306),
        db_name=os.getenv("CLIMSOFT_DB_NAME", "test")
    )


def get_mch_english_connection_string(port_override: str = None) -> str:
    return get_connection_string(
        engine="mysql",
        driver="mysqldb",
        user=os.getenv("MCH_DB_USER", "root"),
        password=os.getenv("MCH_DB_PASSWORD", "password"),
        host=os.getenv("MCH_DB_HOST", "api.opencdms.org"),
        port=os.getenv(
            "MCH_DB_PORT",
            3306
        ) if port_override is None else port_override,
        db_name=os.getenv("MCH_DB_NAME", "test")
    )
