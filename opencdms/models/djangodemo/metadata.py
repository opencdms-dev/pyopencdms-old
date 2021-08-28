from django.db import models
from django.urls import reverse


# Create your models here.
class Obselement(models.Model):
    elementid = models.BigIntegerField(db_column='elementId', primary_key=True)  # Field name made lowercase.
    abbreviation = models.CharField(max_length=255, blank=True, null=True)
    elementname = models.CharField(db_column='elementName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(max_length=255, blank=True, null=True)
    elementscale = models.DecimalField(db_column='elementScale', max_digits=8, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    upperlimit = models.CharField(db_column='upperLimit', max_length=255, blank=True, null=True)  # Field name made lowercase.
    lowerlimit = models.CharField(db_column='lowerLimit', max_length=255, blank=True, null=True)  # Field name made lowercase.
    units = models.CharField(max_length=255, blank=True, null=True)
    elementtype = models.CharField(max_length=50, blank=True, null=True)
    qctotalrequired = models.IntegerField(db_column='qcTotalRequired', blank=True, null=True)  # Field name made lowercase.
    selected = models.IntegerField()

    def get_absolute_url(self):
        return reverse('metadata:obselement-index')

    class Meta:
        managed = True
        db_table = 'obselement'


class Station(models.Model):
    stationid = models.CharField(db_column='stationId', primary_key=True, max_length=255)  # Field name made lowercase.
    stationname = models.CharField(db_column='stationName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    wmoid = models.CharField(max_length=20, blank=True, null=True)
    icaoid = models.CharField(max_length=20, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    qualifier = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    elevation = models.CharField(max_length=255, blank=True, null=True)
    geolocationmethod = models.CharField(db_column='geoLocationMethod', max_length=255, blank=True, null=True)  # Field name made lowercase.
    geolocationaccuracy = models.FloatField(db_column='geoLocationAccuracy', blank=True, null=True)  # Field name made lowercase.
    openingdatetime = models.CharField(db_column='openingDatetime', max_length=50, blank=True, null=True)  # Field name made lowercase.
    closingdatetime = models.CharField(db_column='closingDatetime', max_length=50, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(max_length=50, blank=True, null=True)
    authority = models.CharField(max_length=255, blank=True, null=True)
    adminregion = models.CharField(db_column='adminRegion', max_length=255, blank=True, null=True)  # Field name made lowercase.
    drainagebasin = models.CharField(db_column='drainageBasin', max_length=255, blank=True, null=True)  # Field name made lowercase.
    wacaselection = models.IntegerField(db_column='wacaSelection', blank=True, null=True)  # Field name made lowercase.
    cptselection = models.IntegerField(db_column='cptSelection', blank=True, null=True)  # Field name made lowercase.
    stationoperational = models.IntegerField(db_column='stationOperational', blank=True, null=True)  # Field name made lowercase.

    def get_absolute_url(self):
        return reverse('metadata:station-index')

    class Meta:
        managed = True
        db_table = 'station'
