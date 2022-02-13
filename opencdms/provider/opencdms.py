from typing import Dict, Union, Any
from opencdms.provider.clide import ClideProvider
from opencdms.provider.climsoft import Climsoft4Provider
from opencdms.provider.mch import MCHProvider
from opencdms.provider.midas import MidasProvider
from opencdms.utils.db import midas_session,\
    mch_session, clide_session, climsoft_session


class ProviderConfig:
    def __init__(
        self,
        enable_clide: bool = False,
        enable_climsoft: bool = False,
        enable_mch: bool = False,
        enable_midas: bool = False,
        enable_validation: bool = True
    ):
        self.enable_clide = enable_clide
        self.enable_climsoft = enable_climsoft
        self.enable_mch = enable_mch
        self.enable_midas = enable_midas
        self.enable_validation = enable_validation


class OpenCDMSProvider:
    def __init__(
        self,
        provider_config: ProviderConfig
    ):
        self.clide_provider = ClideProvider() \
            if provider_config.enable_clide else None
        self.climsoft_provider = Climsoft4Provider() \
            if provider_config.enable_climsoft else None
        self.mch_provider = MCHProvider() \
            if provider_config.enable_mch else None
        self.midas_provider = MidasProvider() \
            if provider_config.enable_midas else None

    def create(
        self,
        model_name: str,
        data: Dict
    ):
        response = {
            "clide": None,
            "climsoft": None,
            "mch": None,
            "midas": None
        }
        if self.clide_provider is not None:
            with clide_session() as db_session:
                response["clide"] = self.clide_provider.create(
                    db_session, model_name, data
                )
        if self.climsoft_provider is not None:
            with climsoft_session() as db_session:
                response["climsoft"] = self.climsoft_provider.create(
                    db_session,
                    model_name,
                    data
                )
        if self.mch_provider is not None:
            with mch_session() as db_session:
                response["mch"] = self.mch_provider.create(
                    db_session,
                    model_name,
                    data
                )
        if self.midas_provider is not None:
            with midas_session() as db_session:
                response["midas"] = self.midas_provider.create(
                    db_session,
                    model_name,
                    data
                )

        return response

    def get(self, model_name: str, unique_id: Dict[str, Union[str, int]]):
        response = {
            "clide": None,
            "climsoft": None,
            "mch": None,
            "midas": None
        }

        if self.clide_provider is not None:
            with clide_session() as db_session:
                response["clide"] = self.clide_provider.get(
                    db_session,
                    model_name,
                    unique_id
                )
        if self.climsoft_provider is not None:
            with climsoft_session() as db_session:
                response["climsoft"] = self.climsoft_provider.get(
                    db_session,
                    model_name,
                    unique_id
                )
        if self.mch_provider is not None:
            with mch_session() as db_session:
                response["mch"] = self.mch_provider.get(
                    db_session,
                    model_name,
                    unique_id
                )
        if self.midas_provider is not None:
            with midas_session() as db_session:
                response["midas"] = self.midas_provider.get(
                    db_session,
                    model_name,
                    unique_id
                )

        return response

    def list(
        self,
        model_name: str,
        query: Dict[str, Dict[str, Any]] = None,
        limit: int = 25,
        offset: int = 0
    ):
        response = {
            "clide": None,
            "climsoft": None,
            "mch": None,
            "midas": None
        }

        if self.clide_provider is not None:
            with clide_session() as db_session:
                response["clide"] = self.clide_provider.list(
                    db_session,
                    model_name,
                    query,
                    limit,
                    offset
                )
        if self.climsoft_provider is not None:
            with climsoft_session() as db_session:
                response["climsoft"] = self.climsoft_provider.list(
                    db_session,
                    model_name,
                    query,
                    limit,
                    offset
                )
        if self.mch_provider is not None:
            with mch_session() as db_session:
                response["mch"] = self.mch_provider.list(
                    db_session,
                    model_name,
                    query,
                    limit,
                    offset
                )
        if self.midas_provider is not None:
            with midas_session() as db_session:
                response["midas"] = self.midas_provider.list(
                    db_session,
                    model_name,
                    query,
                    limit,
                    offset
                )
        return response

    def update(
        self,
        model_name: str,
        unique_id: Dict[str, Union[str, int]],
        data: dict
    ):
        response = {
            "clide": None,
            "climsoft": None,
            "mch": None,
            "midas": None
        }

        if self.clide_provider is not None:
            with clide_session() as db_session:
                response["clide"] = self.clide_provider.update(
                    db_session,
                    model_name,
                    unique_id,
                    data
                )
        if self.climsoft_provider is not None:
            with climsoft_session() as db_session:
                response["climsoft"] = self.climsoft_provider.update(
                    db_session,
                    model_name,
                    unique_id,
                    data
                )
        if self.mch_provider is not None:
            with mch_session() as db_session:
                response["mch"] = self.mch_provider.update(
                    db_session,
                    model_name,
                    unique_id,
                    data
                )
        if self.midas_provider is not None:
            with midas_session() as db_session:
                response["midas"] = self.midas_provider.update(
                    db_session,
                    model_name,
                    unique_id,
                    data
                )

        return response

    def delete(self, model_name: str, unique_id: Dict[str, Union[str, int]]):
        response = {
            "clide": None,
            "climsoft": None,
            "mch": None,
            "midas": None
        }

        if self.clide_provider is not None:
            with clide_session() as db_session:
                response["clide"] = self.clide_provider.delete(
                    db_session,
                    model_name,
                    unique_id
                )
        if self.climsoft_provider is not None:
            with climsoft_session() as db_session:
                response["climsoft"] = self.climsoft_provider.delete(
                    db_session,
                    model_name,
                    unique_id
                )
        if self.mch_provider is not None:
            with mch_session() as db_session:
                response["mch"] = self.mch_provider.delete(
                    db_session,
                    model_name,
                    unique_id
                )
        if self.midas_provider is not None:
            with midas_session() as db_session:
                response["midas"] = self.midas_provider.delete(
                    db_session,
                    model_name,
                    unique_id
                )

        return response
