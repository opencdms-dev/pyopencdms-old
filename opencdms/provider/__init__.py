# =================================================================
#
# Authors: Ian Edwards
#
# Copyright (c) 2020, OpenCDMS Project
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

"""A package containing the plugins wrapping CDMS data sources"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from enum import Enum


def get_session_factory(db_uri: str):
    db_engine = create_engine(
        db_uri
    )

    session_factory = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=db_engine
    )

    return session_factory


class QueryOperators(str, Enum):
    gt: str = "__gt__"
    lt: str = "__lt__"
    gte: str = "__ge__"
    lte: str = "__le__"
    equal: str = "__eq__"
    contains: str = "contains"
    not_equal: str = "__ne__"
    ends_with: str = "ends_with"
    starts_with: str = "starts_with"
    identical_to: str = "identical_to"
