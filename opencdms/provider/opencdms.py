from typing import Dict
from sqlalchemy.orm.session import Session
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
        enable_midas: bool = False
    ):
        self.enable_clide = enable_clide
        self.enable_climsoft = enable_climsoft
        self.enable_mch = enable_mch
        self.enable_midas = enable_midas


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
        if self.clide_provider is not None:
            with clide_session() as db_session:
                self.clide_provider.create(db_session, model_name, data)
        if self.climsoft_provider is not None:
            with climsoft_session() as db_session:
                self.climsoft_provider.create(db_session, model_name, data)
        if self.mch_provider is not None:
            with mch_session() as db_session:
                self.mch_provider.create(db_session, model_name, data)
        if self.midas_provider is not None:
            with midas_session() as db_session:
                self.midas_provider.create(db_session, model_name, data)

