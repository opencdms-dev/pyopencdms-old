from pygeoapi.provider.base import (
    BaseProvider,
    ProviderConnectionError,
    ProviderQueryError,
    ProviderItemNotFoundError,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Query, Session
from sqlalchemy.sql import asc, desc
from opencdms.models import cdm as models
from typing import Dict, List
from alchemyjsonschema import SchemaFactory
from alchemyjsonschema import ForeignKeyWalker
from opencdms.utils.db import get_connection_string, get_count
from opencdms.models import surface as models
from opencdms.dtos.observation_schema import (
    ObservationSchema, CreateObservationSchema,
     UpdateObservationSchema, ObservationPygeoapiSchema
)
from shapely import box
from geoalchemy2.shape import from_shape
from pygeoapi.api import LOGGER
from pygeoapi.provider.base import SchemaType
from collections import OrderedDict


class DatabaseConnection:
    """Database connection class to be used as 'with' statement.
    The class returns a connection object.
    """

    def __init__(
        self,
        conn_dic: Dict,
        table: str = None,
        properties: List = None,
        context: str = "query",
    ):
        """
        PostgresProvider Class constructor returning

        :param conn_dic: dictionary with connection parameters
                    to be used by sqlalchemy
            dbname – the database name (database is a deprecated alias)
            user – username used to authenticate
            password – password used to authenticate
            host – database host address
             (defaults to UNIX socket if not provided)
            port – connection port number
             (defaults to 3306 if not provided)

        :param table: table name containing the data. This variable is used to
                assemble column information
        :param properties: User-specified subset of column names to expose
        :param context: query or hits, if query then it will determine
                table column otherwise will not do it
        :returns: DatabaseConnection
        """
        if properties is None:
            self.properties = []
        else:
            self.properties = properties
        self.conn_dic = conn_dic
        self.table = table
        self.context = context
        self.columns = None
        self.fields = {}
        self.session: Session = None
        self.uri = get_connection_string(
            "postgresql",
            "psycopg2",
            self.conn_dic["user"],
            self.conn_dic["password"],
            self.conn_dic["host"],
            self.conn_dic["port"],
            self.conn_dic["dbname"],
        )

    def __enter__(self):
        try:
            self.engine = create_engine(url=self.uri)
            self.session = sessionmaker(bind=self.engine)()
        except Exception as e:
            LOGGER.error(e)
            raise ProviderConnectionError()

        if self.context == "query":
            factory = SchemaFactory(ForeignKeyWalker)
            self.fields = factory(model=models.Observation).get(
                "properties"
            )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


class CDMSProvider(BaseProvider):
    def __init__(self, provider_def):
        super().__init__(provider_def=provider_def)
        self.conn_dic = provider_def["data"]
        self.get_fields()

    def __apply_filters(
        self, query: Query, properties: List = None, bbox: List = None
    ) -> Query:
        if properties is None:
            properties = []

        if bbox is None:
            bbox = []

        for k, v in properties:
            if k in self.fields.keys():
                query = query.filter(
                    getattr(
                        models.Observation,
                        k,
                    )
                    == v
                )

        if type(bbox) == list and len(bbox) == 4:
            min_lng, min_lat, max_lng, max_lat = bbox
            box_polygon = from_shape(box(min_lng, min_lat, max_lng, max_lat),srid=4326)
            query = query.filter(models.Observation.location.ST_Intersects(box_polygon))

        return query


    def _apply_sorting(self, query: Query, sortby: List[Dict]):
        for item in sortby:
            if item['property'] in self.fields.keys():
                sort_attr =  item["property"]
                query = query.order_by(
                    asc(getattr(models.Observation, sort_attr))
                    if item["order"] == "+"
                    else desc(getattr(models.Observation, sort_attr))
                )
        return query


    def get_fields(self):
        """
        Get provider field information (names, types)

        :returns: dict of fields
        """
        if not self.fields:
            with DatabaseConnection(
                self.conn_dic, properties=self.properties
            ) as db:
                self.fields = OrderedDict()
                for k, v in db.fields.items():
                    self.fields[k] = v
        return self.fields

    def get_schema(self, schema_type: SchemaType = SchemaType.item):
        if schema_type in {SchemaType.update, SchemaType.replace}:
            return "application/json", UpdateObservationSchema.schema()
        elif schema_type == SchemaType.create:
            return "application/json", CreateObservationSchema.schema()
        else:
            return "application/json", ObservationPygeoapiSchema.schema()

    def query(
        self,
        startindex: int = 0,
        limit: int = 0,
        resulttype: str = "results",
        bbox: List = None,
        datetime=None,
        properties: List = None,
        sortby: List = None,
        select_properties: List = None,
        skip_geometry: bool = False,
        q: str = None,
        **kwargs,
    ):
        """
        query the provider

        :returns: dict of 0..n GeoJSON features or coverage data
        """

        if bbox is None:
            bbox = []
        if properties is None:
            properties = []
        if sortby is None:
            sortby = []
        if select_properties is None:
            select_properties = []

        if resulttype == "hits":
            with DatabaseConnection(
                conn_dic=self.conn_dic,
                properties=self.properties,
                context="hits",
            ) as db:
                query = db.session.query(models.Observation)

                query = self.__apply_filters(
                    query=query, properties=properties, bbox=bbox
                )

                query = self._apply_sorting(query=query, sortby=sortby)

                return self.__response_feature_hits(get_count(query))

        with DatabaseConnection(
            conn_dic=self.conn_dic, properties=self.properties
        ) as db:
            try:
                query = db.session.query(models.Observation)

                query = self.__apply_filters(
                    query=query, properties=properties, bbox=bbox
                )

                query = self._apply_sorting(query=query, sortby=sortby)

                obs_finals = query.offset(startindex).limit(limit).all()

                include_props = {"code", "measured", "datetime"}

                for p in select_properties:
                    if p in self.get_fields().keys():
                        include_props.add(p)

                feature_collection = {
                    "type": "FeatureCollection",
                    "features": [],
                }

                for obs_final in obs_finals:
                    feature_collection["features"].append(
                        self.__response_feature(
                            obs_final, skip_geometry, include=include_props
                        )
                    )

                return feature_collection
            except Exception as e:
                LOGGER.error(e)
                raise ProviderQueryError()

    def get(self, identifier, **kwargs):
        """
        query the provider by id

        :param identifier: feature id
        :returns: dict of single GeoJSON feature
        """
    
        with DatabaseConnection(
            conn_dic=self.conn_dic, properties=self.properties
        ) as db:
            obs_final = (
                db.session.query(models.Observation)
                .filter_by(
                    id=identifier
                )
                .first()
            )

            if not obs_final:
                raise ProviderItemNotFoundError()

            return self.__response_feature(obs_final)

    def create(self, data):
        """Create a new feature"""
        obs = CreateObservationSchema.parse_raw(data)
        with DatabaseConnection(
            conn_dic=self.conn_dic, properties=self.properties
        ) as db:
            obs_final = models.Observation(**obs.dict())
            db.session.add(obs_final)
            db.session.commit()
        return (
            f"{obs.id}"
        )

    def update(self, identifier, data):
        """Updates an existing feature id with new_feature

        :param identifier: feature id
        :param data: new GeoJSON feature dictionary
        """
        updates = UpdateObservationSchema.parse_raw(data).dict(exclude_unset=True)
        with DatabaseConnection(
            conn_dic=self.conn_dic, properties=self.properties
        ) as db:
            db.session.query(models.Observation).filter_by(
                id=identifier
            ).update(updates)
            db.session.commit()
        return True

    def get_coverage_domainset(self):
        """
        Provide coverage domainset

        :returns: CIS JSON object of domainset metadata
        """

        raise NotImplementedError()

    def get_coverage_rangetype(self):
        """
        Provide coverage rangetype

        :returns: CIS JSON object of rangetype metadata
        """

        raise NotImplementedError()

    def delete(self, identifier):
        """Deletes an existing feature

        :param identifier: feature id
        """
        with DatabaseConnection(
            conn_dic=self.conn_dic, properties=self.properties
        ) as db:
            db.session.query(models.Observation).filter_by(
                id=identifier
            ).delete()
            db.session.commit()
        return True

    def __repr__(self):
        return "<CDMSProvider> {}".format(self.type)

    def __response_feature(self, obs_final, skip_geometry, include: set = None):
        """
        Assembles GeoJSON output from DB query

        :param obs_final: DB row result

        :returns: `dict` of GeoJSON Feature
        """
        obs = ObservationSchema.from_orm(obs_final)

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    obs.coordinates.longitude,
                    obs.coordinates.latitude,
                ],
            } if not skip_geometry else None,
            "properties": obs.dict(by_alias=True) if include is None \
                else obs.dict(include=include, by_alias=True),
            "id": f"{obs.id}"
        }

        return feature

    def __response_feature_hits(self, hits):
        """Assembles GeoJSON/Feature number
        e.g: http://localhost:5000/collections/
        hotosm_bdi_waterways/items?resulttype=hits

        :returns: GeoJSON FeaturesCollection
        """

        feature_collection = {
            "features": [],
            "type": "FeatureCollection",
            "numberMatched": hits,
        }

        return feature_collection
