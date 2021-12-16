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
from typing import Dict, Any, Union, List
from types import ModuleType
from sqlalchemy.orm.session import Session
from importlib import import_module

LOGGER = logging.getLogger(__name__)


class FailedCreatingModel(Exception):
    pass


class FailedGettingModel(Exception):
    pass


class QueryFailedForModel(Exception):
    pass


class FailedUpdatingModel(Exception):
    pass


class FailedDeletingModel(Exception):
    pass


class FailedSoftDeletingModel(Exception):
    pass


class CDMSProvider:
    """Generic CDMS Provider Abstract Base Class"""

    def __init__(
        self,
        models: ModuleType,
        schemas: ModuleType
    ):
        self.models = models
        self.schemas = schemas

    def create(
        self,
        db_session: Session,
        model_name: str,
        data: Dict
    ) -> Any:

        try:
            model = getattr(self.models, model_name)

            input_data = getattr(
                import_module(
                    f"{self.schemas.__name__}.{model_name.lower()}"
                ),
                f"Create{model_name}"
            )(**data)

            instance = model(**input_data.dict())
            db_session.add(instance)
            db_session.commit()
            return instance
        except Exception as e:
            db_session.rollback()
            LOGGER.exception(e)
            raise FailedCreatingModel(
                f"Failed creating Clide model: {model_name}, with error: {e}"
            )

    def get(
        self,
        db_session: Session,
        model_name: str,
        unique_id: Dict[str, Union[str, int]]
    ):
        # validate required unique id
        getattr(
            import_module(f"{self.schemas.__name__}.{model_name.lower()}"),
            f"UniqueId"
        )
        try:
            model = getattr(self.models, model_name)
            instance = db_session.query(model) \
                .filter_by(**unique_id).first()
            return instance
        except Exception as e:
            LOGGER.exception(e)
            raise FailedGettingModel(
                f"Failed getting Clide model: {model_name}"
                f" with key(s): {unique_id}"
            )

    def list(
        self,
        db_session: Session,
        model_name: str,
        query: Dict[str, Dict[str, Any]] = None,
        limit: int = 25,
        offset: int = 0
    ) -> List[Any]:

        try:
            model = getattr(self.models, model_name)
            q = db_session.query(model)

            if query is not None:
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
            raise QueryFailedForModel(
                f"Query failed for Clide model: {model_name} "
                f"for query: {query}"
            )

    def update(
        self,
        db_session: Session,
        model_name: str,
        unique_id: Dict[str, Union[str, int]],
        data: dict
    ):
        # validate required unique id
        getattr(
            import_module(f"{self.schemas.__name__}.{model_name.lower()}"),
            f"UniqueId"
        )

        try:
            model = getattr(self.models, model_name)
            input_data = getattr(
                import_module(
                    f"{self.schemas.__name__}.{model_name.lower()}"
                ),
                f"Update{model_name}"
            )(**data)

            db_session.query(model)\
                .filter_by(**unique_id).update(input_data.dict())
            db_session.commit()

            updated_instance = db_session.query(model)\
                .filter_by(**unique_id).first()

            return updated_instance
        except Exception as e:
            db_session.rollback()
            LOGGER.exception(e)
            raise FailedUpdatingModel(
                f"Failed updating Clide model: {model_name} "
                f"with updates: {data}"
            )

    def delete(
        self,
        db_session: Session,
        model_name: str,
        unique_id: Dict[str, Union[str, int]]
    ):
        # validate required unique id
        getattr(
            import_module(f"{self.schemas.__name__}.{model_name.lower()}"),
            f"UniqueId"
        )

        try:
            model = getattr(self.models, model_name)
            db_session.query(model).filter_by(**unique_id).delete()
            db_session.commit()
            return unique_id
        except Exception as e:
            db_session.rollback()
            LOGGER.exception(e)
            raise FailedDeletingModel(
                f"Failed deleting Clide model: {model_name}"
                f"with unique_id: {unique_id}"
            )

    # @abstractmethod def before_update(self, model_name: str, unique_id:
    # Dict[str, Union[str, int]], data: dict): raise NotImplementedError
    #
    # @abstractmethod def after_update(self, model_name: str, unique_id:
    # Dict[str, Union[str, int]], data: dict): raise NotImplementedError
    #
    # @abstractmethod
    # def before_create(self, model_name: str, data: dict):
    #     raise NotImplementedError
    #
    # @abstractmethod
    # def after_create(self, model_name: str, data: dict):
    #     raise NotImplementedError
