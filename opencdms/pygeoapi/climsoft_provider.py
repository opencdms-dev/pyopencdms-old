import logging
import json

from psycopg2.sql import SQL, Identifier
from pygeoapi.provider.base import (
    BaseProvider,
    ProviderConnectionError,
    ProviderQueryError,
    ProviderItemNotFoundError
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Query, joinedload
from sqlalchemy.sql import asc, desc
from typing import Dict, List
from alchemyjsonschema import SchemaFactory
from alchemyjsonschema import ForeignKeyWalker
from opencdms.utils.db import get_connection_string, get_count
from opencdms.models.climsoft import v4_1_1_core as models


LOGGER = logging.getLogger(__name__)


class DatabaseConnection:
    """Database connection class to be used as 'with' statement.
    The class returns a connection object.
    """

    def __init__(
        self,
        conn_dic: Dict,
        table: str = None,
        properties: List = None,
        context: str = "query"
    ):
        """
        MySQLProvider Class constructor returning

        :param conn: dictionary with connection parameters
                    to be used by sqlalchemy
            dbname – the database name (database is a deprecated alias)
            user – user name used to authenticate
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
        self.session = None
        self.uri = get_connection_string(
            "mysql",
            "mysqldb",
            self.conn_dic["user"],
            self.conn_dic["password"],
            self.conn_dic["host"],
            self.conn_dic["port"],
            self.conn_dic["dbname"]
        )

    def __enter__(self):
        try:
            self.engine = create_engine(
                url=self.uri
            )
            self.session = sessionmaker(
                bind=self.engine
            )()
        except Exception as e:
            LOGGER.error(e)
            raise ProviderConnectionError()

        if self.context == 'query':
            factory = SchemaFactory(ForeignKeyWalker)
            self.fields = {
                k: v['type']
                for k, v in factory(
                    model=models.Observationfinal
                ).get("properties").items()
            }
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


class ClimsoftProvider(BaseProvider):
    def __init__(self, provider_def):
        super().__init__(provider_def=provider_def)

        # self.table = provider_def['table']
        # self.id_field = provider_def['id_field']
        self.conn_dic = provider_def['data']
        # self.geom = provider_def.get('geom_field', 'geom')
        self.get_fields()

    def __apply_filters(
        self,
        query: Query,
        properties: List = None,
        bbox: List = None
    ) -> Query:
        if properties is None:
            properties = []
            for k, v in properties:
                query = query.filter_by(k=v)

        return query

    def _apply_sorting(self, query: Query, sortby: List[Dict]):
        for item in sortby:
            query.order_by(
                asc(item['property']) if item['order'] == '+'
                else desc(item['property'])
            )
        return query

    def get_fields(self):
        """
        Get provider field information (names, types)

        :returns: dict of fields
        """
        if not self.fields:
            with DatabaseConnection(
                self.conn_dic,
                properties=self.properties
            ) as db:
                self.fields = db.fields
        return self.fields

    def get_data_path(self, baseurl, urlpath, dirpath):
        """
        Gets directory listing or file description or raw file dump

        :param baseurl: base URL of endpoint
        :param urlpath: base path of URL
        :param dirpath: directory basepath (equivalent of URL)

        :returns: `dict` of file listing or `dict` of GeoJSON item or raw file
        """

        raise NotImplementedError()

    def get_metadata(self):
        """
        Provide data/file metadata

        :returns: `dict` of metadata construct (format
                  determined by provider/standard)
        """

        raise NotImplementedError()

    def query(
        self,
        startindex: int = 0,
        limit: int = 0,
        resulttype: str = 'results',
        bbox: List = None,
        datetime_=None,
        properties: List = None,
        sortby: List = None,
        select_properties: List = None,
        skip_geometry: bool = False,
        q: str = None,
        **kwargs
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

        if resulttype == 'hits':
            with DatabaseConnection(
                conn_dic=self.conn_dic,
                properties=self.properties,
                context='hits'
            ) as db:
                query = db.session.query(
                    models.Observationfinal
                )

                query = self.__apply_filters(
                    query=query,
                    properties=properties,
                    bbox=bbox
                )

                return self.__response_feature_hits(get_count(query))

        with DatabaseConnection(
            conn_dic=self.conn_dic,
            properties=self.properties
        ) as db:
            row_data = db.session.query(models.Observationfinal).options(
                joinedload(models.Observationfinal.station)
            ).all()
            feature_collection = {
                "type": "FeatureCollection",
                "features": []
            }

            for rd in row_data:
                feature_collection["features"].append(
                    self.__response_feature(rd)
                )

            return feature_collection

    def get(self, identifier):
        """
        query the provider by id

        :param identifier: feature id
        :returns: dict of single GeoJSON feature
        """

        raise NotImplementedError()

    def create(self, new_feature):
        """Create a new feature
        """

        raise NotImplementedError()

    def update(self, identifier, new_feature):
        """Updates an existing feature id with new_feature

        :param identifier: feature id
        :param new_feature: new GeoJSON feature dictionary
        """

        raise NotImplementedError()

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

        raise NotImplementedError()

    def __repr__(self):
        return '<ClimsoftProvider> {}'.format(self.type)

    def __response_feature(self, row_data):
        """
        Assembles GeoJSON output from DB query

        :param row_data: DB row result

        :returns: `dict` of GeoJSON Feature
        """

        if row_data:
            rd = row_data.__dict__
            rd.pop('_sa_instance_state')
            rd = {
                **rd,
                "station": rd.get("station").__dict__
                if rd.get("station") else None
            }
            feature = {
                'type': 'Feature'
            }

            geom = rd.pop('st_asgeojson') if rd.get('st_asgeojson') else None

            feature['geometry'] = json.loads(
                geom
            ) if geom is not None else None  # noqa

            feature['properties'] = rd
            feature['id'] = feature['properties'].get(self.id_field)

            return feature
        else:
            return None

    def __response_feature_hits(self, hits):
        """Assembles GeoJSON/Feature number
        e.g: http://localhost:5000/collections/
        hotosm_bdi_waterways/items?resulttype=hits

        :returns: GeoJSON FeaturesCollection
        """

        feature_collection = {
            "features": [],
            "type": "FeatureCollection",
            'numberMatched': hits
        }

        return feature_collection



