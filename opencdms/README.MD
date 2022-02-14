# pygeoapi concepts

Here is a pygeoapi config file as an example and high-level overview of the concepts.

```yaml
server:
  bind:
      host: 0.0.0.0  # listening address for incoming connections
      port: 5000  # listening port for incoming connections
  url: http://localhost:5000/  # url of server
  mimetype: application/json; charset=UTF-8  # default MIME type
  encoding: utf-8  # default server encoding
  language: en-US  # default server language
  gzip: false # default server config to gzip/compress responses to requests with gzip in the Accept-Encoding header
  cors: true  # boolean on whether server should support CORS
  pretty_print: true  # whether JSON responses should be pretty-printed
  limit: 10  # server limit on number of items to return

  templates: # optional configuration to specify a different set of templates for HTML pages. Recommend using absolute paths. Omit this to use the default provided templates
    path: /path/to/jinja2/templates/folder # path to templates folder containing the jinja2 template HTML files
    static: /path/to/static/folder # path to static folder containing css, js, images and other static files referenced by the template

  map:  # leaflet map setup for HTML pages
      url: https://maps.wikimedia.org/osm-intl/{z}/{x}/{y}.png
      attribution: '<a href="https://wikimediafoundation.org/wiki/Maps_Terms_of_Use">Wikimedia maps</a> | Map data &copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
  ogc_schemas_location: /opt/schemas.opengis.net  # local copy of http://schemas.opengis.net

  manager:  # optional OGC API - Processes asynchronous job management
      name: TinyDB  # plugin name (see pygeoapi.plugin for supported process_manager's)
      connection: /tmp/pygeoapi-process-manager.db  # connection info to store jobs (e.g. filepath)
      output_dir: /tmp/  # temporary file area for storing job results (files)

logging:
    level: ERROR  # the logging level (see https://docs.python.org/3/library/logging.html#logging-levels)
    logfile: /path/to/pygeoapi.log  # the full file path to the logfile

metadata:
    identification:
        title: pygeoapi default instance  # the title of the service
        description: pygeoapi provides an API to geospatial data  # some descriptive text about the service
        keywords:  # list of keywords about the service
            - geospatial
            - data
            - api
        keywords_type: theme  # keyword type as per the ISO 19115 MD_KeywordTypeCode codelist. Accepted values are discipline, temporal, place, theme, stratum
        terms_of_service: https://creativecommons.org/licenses/by/4.0/  # terms of service
        url: http://example.org  # informative URL about the service
    license:  # licensing details
        name: CC-BY 4.0 license
        url: https://creativecommons.org/licenses/by/4.0/
    provider:  # service provider details
        name: Organization Name
        url: https://pygeoapi.io
    contact:  # service contact details
        name: Lastname, Firstname
        position: Position Title
        address: Mailing Address
        city: City
        stateorprovince: Administrative Area
        postalcode: Zip or Postal Code
        country: Country
        phone: +xx-xxx-xxx-xxxx
        fax: +xx-xxx-xxx-xxxx
        email: you@example.org
        url: Contact URL
        hours: Mo-Fr 08:00-17:00
        instructions: During hours of service. Off on weekends.
        role: pointOfContact

resources:
    obs:
        type: collection  # REQUIRED (collection, process, or stac-collection)
        title: Observations  # title of dataset
        description: My cool observations  # abstract of dataset
        keywords:  # list of related keywords
            - observations
            - monitoring
        context:  # linked data configuration (see Linked Data section)
            - datetime: https://schema.org/DateTime
            - vocab: https://example.com/vocab#
              stn_id: "vocab:stn_id"
              value: "vocab:value"
        links:  # list of 1..n related links
            - type: text/csv  # MIME type
              rel: canonical  # link relations per https://www.iana.org/assignments/link-relations/link-relations.xhtml
              title: data  # title
              href: https://github.com/mapserver/mapserver/blob/branch-7-0/msautotest/wxs/data/obs.csv  # URL
              hreflang: en-US  # language
        extents:  # spatial and temporal extents
            spatial:  # required
                bbox: [-180,-90,180,90]  # list of minx, miny, maxx, maxy
                crs: http://www.opengis.net/def/crs/OGC/1.3/CRS84  # CRS
            temporal:  # optional
                begin: 2000-10-30T18:24:39Z  # start datetime in RFC3339
                end: 2007-10-30T08:57:29Z  # end datetime in RFC3339
        providers:  # list of 1..n required connections information
            # provider name
            # see pygeoapi.plugin for supported providers
            # for custom built plugins, use the import path (e.g. mypackage.provider.MyProvider)
            # see Plugins section for more information
#            - type: feature
#              default: true
#              name: Climsoft
#
            - type: feature # underlying data geospatial type: (allowed values are: feature, coverage, record, tile, edr)
              default: true  # optional: if not specified, the first provider definition is considered the default
              name: CSV
              data: tests/data/obs.csv  # required: the data filesystem path or URL, depending on plugin setup
              id_field: id  # required for vector data, the field corresponding to the ID
              uri_field: uri # optional field corresponding to the Uniform Resource Identifier (see Linked Data section)
              time_field: datetimestamp  # optional field corresponding to the temporal property of the dataset
              title_field: foo # optional field of which property to display as title/label on HTML pages
              format:  # optional default format
                  name: GeoJSON  # required: format name
                  mimetype: application/json  # required: format mimetype
              options:  # optional options to pass to provider (i.e. GDAL creation)
                  option_name: option_value
              properties:  # optional: only return the following properties, in order
                  - stn_id
                  - value

    hello-world:  # name of process
        type: collection  # REQUIRED (collection, process, or stac-collection)
        processor:
            name: HelloWorld  # Python path of process defition
```

### Types of providers and when to use which one

We will be using `feature` type provider for the time being.

- ***feature:*** https://www.ogc.org/standards/ogcapi-features
- ***coverage:*** https://github.com/opengeospatial/ogcapi-coverages
- ***record:*** https://github.com/opengeospatial/ogcapi-records
- ***tile:*** https://github.com/opengeospatial/ogcapi-tiles
- ***edr:*** https://github.com/opengeospatial/ogcapi-environmental-data-retrieval

# Confusion
`pygeoapi` assumes that features are data types (equivalent to `table` in SQL).
so, when we add a feature type resource. It is available under collections as a single entity.

So, if we add a feature called `climsoft` in pygeoapi resources. `climsoft
 is expected to be a single table. But in reality, climsoft is a collection of tables
with internal business logics.

Now, when a user want to add `climsoft` CDMS using opencdms pygeoapi provider plugin,
should we generate a list of features that will be configured for climsoft tables?
