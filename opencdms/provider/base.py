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
from typing import Dict, Any, Union
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
            input_data = getattr(getattr(
                import_module(
                    f"{self.schemas.__name__}.{model_name.lower()}"
                ),
                f"Create{model_name}"
            ), "parse_obj")(data)
            print(input_data)
            orm_parser = getattr(getattr(
                import_module(
                    f"{self.schemas.__name__}.{model_name.lower()}"
                ),
                model_name
            ), "from_orm")

            instance = model(**input_data.dict())
            db_session.add(instance)
            db_session.commit()
            return orm_parser(instance)
        except AttributeError as e:
            return e
        except Exception as e:
            db_session.rollback()
            LOGGER.exception(e)
            raise FailedCreatingModel(
                f"Failed creating model "
                f"in module: {self.models.__name__}, "
                f"model name: {model_name}, "
                f"with error: {e}"
            )

    def get(
        self,
        db_session: Session,
        model_name: str,
        unique_id: Dict[str, Union[str, int]]
    ):
        # validate required unique id

        unique_id_validated_fields = getattr(
            getattr(
                import_module(f"{self.schemas.__name__}.{model_name.lower()}"),
                "UniqueId"
            ),
            "parse_obj"
        )(unique_id).dict()

        try:
            model = getattr(self.models, model_name)

            orm_parser = getattr(getattr(
                import_module(
                    f"{self.schemas.__name__}.{model_name.lower()}"
                ),
                model_name
            ), "from_orm")

            instance = db_session.query(model) \
                .filter_by(**unique_id_validated_fields).first()
            return orm_parser(instance)
        except AttributeError as e:
            return e
        except Exception as e:
            LOGGER.exception(e)
            raise FailedGettingModel(
                f"Failed getting model "
                f"in module: {self.models.__name__}, "
                f"model name: {model_name}, "
                f"with key(s): {unique_id} "
                f"with error: {e} "
            )

    def list(
        self,
        db_session: Session,
        model_name: str,
        query: Dict[str, Dict[str, Any]] = None,
        limit: int = 25,
        offset: int = 0
    ):

        try:
            model = getattr(self.models, model_name)

            orm_parser = getattr(getattr(
                import_module(
                    f"{self.schemas.__name__}.{model_name.lower()}"
                ),
                model_name
            ), "from_orm")

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

            return [
                orm_parser(li) for li in q.offset(offset).limit(limit).all()
            ]
        except AttributeError as e:
            return e
        except Exception as e:
            LOGGER.exception(e)
            raise QueryFailedForModel(
                f"Query failed "
                f"in module: {self.models.__name__}, "
                f"for query: {query}, "
                f"with error: {e}"
            )

    def update(
        self,
        db_session: Session,
        model_name: str,
        unique_id: Dict[str, Union[str, int]],
        data: dict
    ):
        # validate required unique id
        unique_id_validated_fields = getattr(
            getattr(
                import_module(f"{self.schemas.__name__}.{model_name.lower()}"),
                "UniqueId"
            ),
            "parse_obj"
        )(unique_id).dict()

        data = dict(filter(lambda kv: kv[1] is not None, data.items()))

        try:
            model = getattr(self.models, model_name)
            input_data = getattr(getattr(
                import_module(
                    f"{self.schemas.__name__}.{model_name.lower()}"
                ),
                f"Update{model_name}"
            ), "parse_obj")(data)

            orm_parser = getattr(getattr(
                import_module(
                    f"{self.schemas.__name__}.{model_name.lower()}"
                ),
                model_name
            ), "from_orm")

            db_session.query(model)\
                .filter_by(**unique_id_validated_fields)\
                .update(input_data.dict())
            db_session.commit()

            updated_instance = db_session.query(model)\
                .filter_by(**unique_id_validated_fields)\
                .first()

            return orm_parser(updated_instance)
        except AttributeError as e:
            return e
        except Exception as e:
            db_session.rollback()
            LOGGER.exception(e)
            raise FailedUpdatingModel(
                f"Failed updating model "
                f"in module: {self.models.__name__} "
                f"model name: {model_name} "
                f"with updates: {data}, "
                f"with error: {e}"
            )

    def delete(
        self,
        db_session: Session,
        model_name: str,
        unique_id: Dict[str, Union[str, int]]
    ):
        # validate required unique id
        unique_id_validated_fields = getattr(
            getattr(
                import_module(f"{self.schemas.__name__}.{model_name.lower()}"),
                "UniqueId"
            ),
            "parse_obj"
        )(unique_id).dict()

        try:
            model = getattr(self.models, model_name)
            db_session.query(model)\
                .filter_by(**unique_id_validated_fields).delete()
            db_session.commit()
            return unique_id
        except Exception as e:
            db_session.rollback()
            LOGGER.exception(e)
            raise FailedDeletingModel(
                f"Failed deleting model "
                f"in module: {self.models.__name__} "
                f"model name: {model_name}, "
                f"with unique_id: {unique_id}, "
                f"with error: {e}"
            )
