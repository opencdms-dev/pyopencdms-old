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

import logging
from abc import ABC
from typing import Dict, Any, Union, List
from sqlalchemy.orm.session import Session
from .base import CDMSProvider
from . import get_session_factory
from opencdms.models import clide as clide_models

LOGGER = logging.getLogger(__name__)


class FailedCreatingClideModel(Exception):
    pass


class FailedGettingClideModel(Exception):
    pass


class QueryFailedForClideModel(Exception):
    pass


class FailedUpdatingClideModel(Exception):
    pass


class FailedDeletingClideModel(Exception):
    pass


class FailedSoftDeletingClideModel(Exception):
    pass


class Clide(CDMSProvider, ABC):
    def __init__(self, db_conn_str: str):
        session_factory = get_session_factory(db_uri=db_conn_str)
        self.db_session: Session = session_factory()

    def create(self, model_name: str, data: Dict) -> Any:
        try:
            model = getattr(clide_models, model_name)
            instance = model(**data)
            self.db_session.add(instance)
            self.db_session.commit()
            return instance
        except Exception as e:
            self.db_session.rollback()
            LOGGER.exception(e)
            raise FailedCreatingClideModel(
                f"Failed creating Clide model: {model_name}, with error: {e}"
            )

    def get(self, model_name: str, unique_id: Dict[str, Union[str, int]]):
        try:
            model = getattr(clide_models, model_name)
            instance = self.db_session.query(model) \
                .filter_by(**unique_id).first()
            return instance
        except Exception as e:
            LOGGER.exception(e)
            raise FailedGettingClideModel(
                f"Failed getting Clide model: {model_name}"
                f" with key(s): {unique_id}"
            )

    def list(
        self,
        model_name: str,
        query: Dict[str, Dict[str, Any]],
        limit: 25,
        offset: 0
    ) -> List[Any]:
        try:
            model = getattr(clide_models, model_name)
            q = self.db_session.query(model)

            for k, v in query.items():
                column = k
                operator = v["operator"]
                value = v.get("value")

                if operator in {"__gt__", "__lt__", "__ge__",
                                "__le__", "__eq__", "__ne__"}:
                    q = q.filter(
                        getattr(
                            getattr(model, column),
                            operator
                        )(value))  # Model.column.operator(value)
                elif operator == "contains":
                    q = q.filter(
                        getattr(
                            getattr(model, column),
                            "ilike"
                        )(f"%{value}%")  # Model.column.ilike(%value%)
                    )
                elif operator == "starts_with":
                    q = q.filter(
                        getattr(
                            getattr(model, column),  # Model.column
                            "ilike"
                        )(f"{value}%")  # Model.column.ilike(value%)
                    )
                elif operator == "ends_with":
                    q = q.filter(
                        getattr(
                            getattr(model, column),  # Model.column
                            "ilike"
                        )(f"%{value}")  # Model.column.ilike(%value)
                    )
                else:
                    raise NotImplementedError
            return q.offset(offset).limit(limit).all()
        except Exception as e:
            LOGGER.exception(e)
            raise QueryFailedForClideModel(f"Query failed for "
                                           f"Clide model: {model_name} "
                                           f"for query: {query}")

    def update(
        self,
        model_name: str,
        unique_id: Dict[str, Union[str, int]],
        data: dict
    ):
        try:
            model = getattr(clide_models, model_name)
            self.db_session.query(model).filter_by(**unique_id).update(data)
            self.db_session.commit()
            updated_instance = self.db_session.query(model)\
                .filter_by(**unique_id).first()

            return updated_instance
        except Exception as e:
            self.db_session.rollback()
            LOGGER.exception(e)
            raise FailedUpdatingClideModel(
                f"Failed updating Clide model: {model_name} "
                f"with updates: {data}"
            )

    def delete(
        self,
        model_name: str,
        unique_id: Dict[str, Union[str, int]]
    ):
        try:
            model = getattr(clide_models, model_name)
            self.db_session.query(model).filter_by(unique_id).delete()
            self.db_session.commit()
            return unique_id
        except Exception as e:
            self.db_session.rollback()
            LOGGER.exception(e)
            raise FailedDeletingClideModel(
                f"Failed deleting Clide model: {model_name}"
                f"with unique_id: {unique_id}"
            )
