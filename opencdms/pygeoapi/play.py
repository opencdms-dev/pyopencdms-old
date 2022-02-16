import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Query, joinedload
from sqlalchemy.sql import asc, desc
from typing import Dict, List
from opencdms.utils.db import get_connection_string, get_count
from opencdms.models.climsoft import v4_1_1_core as models


if __name__ == "__main__":
    uri = get_connection_string(
        "mysql",
        "mysqldb",
        "root",
        "password",
        "127.0.0.1",
        "23306",
        "mariadb_climsoft_test_db_v4"
    )
    engine = create_engine(
        url=uri
    )
    session = sessionmaker(
        bind=engine
    )()

    result = {
        column.key: column.type.get_dbapi_type(
            engine.dialect.dbapi
        )
        for column in models.Observationfinal.__table__.columns
    }

    fields = {}

    for k, v in result.items():
        fields[k] = {'type': v}

    print(json.dumps(fields, indent=2, default=str))

