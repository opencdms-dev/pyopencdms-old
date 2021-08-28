"""
The models below were originally created by Django's `inspectdb`
by inspecting the original Climsoft 4 database.

However, the original tables did not have a single-column primary
key therefore `inspectdb` incorrectly set `stationid` as the primary
key in each case, and represented the rest of the composite key
using `unique_together`.

This would fail when duplicates station id's were entered,
therefore an additional AutoField called `id` as been added to
each.

`primary_key` has been removed from each `stationid` and
`managed` has been changed from False to True.

We've retained separated `yyyy`, `mm` and `dd` fields to manage
required date parts and partial dates in the same way as the desktop
software.

In form_daily2 there are fields for temperature, precipitation,
cloud height and visibility units. We've just retained these for now
and added the valid and default choices to the fields.

Text fields in the original database were permitted to be NULL (in
addition to just empty "" by default) therefore the CharField fields
below currently have `null=True` created by `inspectdb`.

A foreign key to the User table has been added to track the user who
submits the form. The username will also be stored in the legacy
`signature` field for consistency with Climsoft Desktop.
If the user is deleted the key entry record gets disowned (the user
becomes NULL).

"""
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Defaults
DEG_C = 'Deg C'
MM = 'mm'
FEET = 'feet'
METRES = 'metres'


# Units choices
TEMP = [(DEG_C, 'Deg C'), ('Deg F', 'Deg F')]
PRECIP = [(MM, 'mm'), ('inches', 'inches')]
CLOUD = [(FEET, 'feet'), ('metres', 'metres')]
VIS = [(METRES, 'metres'),('yards', 'yards')]

# Flags choices:
# M (Missing), the data value is missing;
# T (Trace), the data value has been recorded as zero but a small trace was observed;
# E (Estimated), the data value is an estimated value rather than an observed value.
# G (Generated), the data has been generated from other values.
# D (Dubious), Dubious or suspect value (data).
FLAGS = [('', ''), ('M', 'M'), ('T', 'T'), ('E', 'E'), ('G', 'G'), ('D', 'D')]


class KeyEntryModel(models.Model):
    class Meta:
        abstract = True


class FormHourly(KeyEntryModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    stationid = models.CharField(db_column='stationId', max_length=50)  # Field name made lowercase.
    elementid = models.IntegerField(db_column='elementId')  # Field name made lowercase.
    yyyy = models.IntegerField()
    mm = models.IntegerField()
    dd = models.IntegerField()

    hh_00 = models.CharField(max_length=50, blank=True, null=True)
    hh_01 = models.CharField(max_length=50, blank=True, null=True)
    hh_02 = models.CharField(max_length=50, blank=True, null=True)
    hh_03 = models.CharField(max_length=50, blank=True, null=True)
    hh_04 = models.CharField(max_length=50, blank=True, null=True)
    hh_05 = models.CharField(max_length=50, blank=True, null=True)
    hh_06 = models.CharField(max_length=50, blank=True, null=True)
    hh_07 = models.CharField(max_length=50, blank=True, null=True)
    hh_08 = models.CharField(max_length=50, blank=True, null=True)
    hh_09 = models.CharField(max_length=50, blank=True, null=True)
    hh_10 = models.CharField(max_length=50, blank=True, null=True)
    hh_11 = models.CharField(max_length=50, blank=True, null=True)
    hh_12 = models.CharField(max_length=50, blank=True, null=True)
    hh_13 = models.CharField(max_length=50, blank=True, null=True)
    hh_14 = models.CharField(max_length=50, blank=True, null=True)
    hh_15 = models.CharField(max_length=50, blank=True, null=True)
    hh_16 = models.CharField(max_length=50, blank=True, null=True)
    hh_17 = models.CharField(max_length=50, blank=True, null=True)
    hh_18 = models.CharField(max_length=50, blank=True, null=True)
    hh_19 = models.CharField(max_length=50, blank=True, null=True)
    hh_20 = models.CharField(max_length=50, blank=True, null=True)
    hh_21 = models.CharField(max_length=50, blank=True, null=True)
    hh_22 = models.CharField(max_length=50, blank=True, null=True)
    hh_23 = models.CharField(max_length=50, blank=True, null=True)
    flag00 = models.CharField(max_length=50, blank=True, null=True, choices=FLAGS)
    flag01 = models.CharField(max_length=50, blank=True, null=True, choices=FLAGS)
    flag02 = models.CharField(max_length=50, blank=True, null=True, choices=FLAGS)
    flag03 = models.CharField(max_length=50, blank=True, null=True, choices=FLAGS)
    flag04 = models.CharField(max_length=50, blank=True, null=True, choices=FLAGS)
    flag05 = models.CharField(max_length=50, blank=True, null=True, choices=FLAGS)
    flag06 = models.CharField(max_length=50, blank=True, null=True, choices=FLAGS)
    flag07 = models.CharField(max_length=50, blank=True, null=True, choices=FLAGS)
    flag08 = models.CharField(max_length=50, blank=True, null=True, choices=FLAGS)
    flag09 = models.CharField(max_length=50, blank=True, null=True, choices=FLAGS)
    flag10 = models.CharField(max_length=50, blank=True, null=True, choices=FLAGS)
    flag11 = models.CharField(max_length=50, blank=True, null=True, choices=FLAGS)
    flag12 = models.CharField(max_length=50, blank=True, null=True, choices=FLAGS)
    flag13 = models.CharField(max_length=50, blank=True, null=True, choices=FLAGS)
    flag14 = models.CharField(max_length=50, blank=True, null=True, choices=FLAGS)
    flag15 = models.CharField(max_length=50, blank=True, null=True, choices=FLAGS)
    flag16 = models.CharField(max_length=50, blank=True, null=True, choices=FLAGS)
    flag17 = models.CharField(max_length=50, blank=True, null=True, choices=FLAGS)
    flag18 = models.CharField(max_length=50, blank=True, null=True, choices=FLAGS)
    flag19 = models.CharField(max_length=50, blank=True, null=True, choices=FLAGS)
    flag20 = models.CharField(max_length=50, blank=True, null=True, choices=FLAGS)
    flag21 = models.CharField(max_length=50, blank=True, null=True, choices=FLAGS)
    flag22 = models.CharField(max_length=50, blank=True, null=True, choices=FLAGS)
    flag23 = models.CharField(max_length=50, blank=True, null=True, choices=FLAGS)
    total = models.CharField(max_length=50, blank=True, null=True)
    signature = models.CharField(max_length=50, blank=True, null=True)
    entrydatetime = models.DateTimeField(db_column='entryDatetime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'form_hourly'
        unique_together = (('stationid', 'elementid', 'yyyy', 'mm', 'dd'),)

    def get_absolute_url(self):
        return reverse('keyentry:form_hourly')


class FormDaily2(KeyEntryModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    stationid = models.CharField(db_column='stationId', max_length=50)  # Field name made lowercase.
    elementid = models.IntegerField(db_column='elementId')  # Field name made lowercase.
    yyyy = models.IntegerField()
    mm = models.IntegerField()
    hh = models.IntegerField()
    day01 = models.CharField(max_length=45, blank=True, null=True)
    day02 = models.CharField(max_length=45, blank=True, null=True)
    day03 = models.CharField(max_length=45, blank=True, null=True)
    day04 = models.CharField(max_length=45, blank=True, null=True)
    day05 = models.CharField(max_length=45, blank=True, null=True)
    day06 = models.CharField(max_length=45, blank=True, null=True)
    day07 = models.CharField(max_length=45, blank=True, null=True)
    day08 = models.CharField(max_length=45, blank=True, null=True)
    day09 = models.CharField(max_length=45, blank=True, null=True)
    day10 = models.CharField(max_length=45, blank=True, null=True)
    day11 = models.CharField(max_length=45, blank=True, null=True)
    day12 = models.CharField(max_length=45, blank=True, null=True)
    day13 = models.CharField(max_length=45, blank=True, null=True)
    day14 = models.CharField(max_length=45, blank=True, null=True)
    day15 = models.CharField(max_length=45, blank=True, null=True)
    day16 = models.CharField(max_length=45, blank=True, null=True)
    day17 = models.CharField(max_length=45, blank=True, null=True)
    day18 = models.CharField(max_length=45, blank=True, null=True)
    day19 = models.CharField(max_length=45, blank=True, null=True)
    day20 = models.CharField(max_length=45, blank=True, null=True)
    day21 = models.CharField(max_length=45, blank=True, null=True)
    day22 = models.CharField(max_length=45, blank=True, null=True)
    day23 = models.CharField(max_length=45, blank=True, null=True)
    day24 = models.CharField(max_length=45, blank=True, null=True)
    day25 = models.CharField(max_length=45, blank=True, null=True)
    day26 = models.CharField(max_length=45, blank=True, null=True)
    day27 = models.CharField(max_length=45, blank=True, null=True)
    day28 = models.CharField(max_length=45, blank=True, null=True)
    day29 = models.CharField(max_length=45, blank=True, null=True)
    day30 = models.CharField(max_length=45, blank=True, null=True)
    day31 = models.CharField(max_length=45, blank=True, null=True)
    flag01 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    flag02 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    flag03 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    flag04 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    flag05 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    flag06 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    flag07 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    flag08 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    flag09 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    flag10 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    flag11 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    flag12 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    flag13 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    flag14 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    flag15 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    flag16 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    flag17 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    flag18 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    flag19 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    flag20 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    flag21 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    flag22 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    flag23 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    flag24 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    flag25 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    flag26 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    flag27 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    flag28 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    flag29 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    flag30 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    flag31 = models.CharField(max_length=1, blank=True, null=True, choices=FLAGS)
    period01 = models.CharField(max_length=45, blank=True, null=True)
    period02 = models.CharField(max_length=45, blank=True, null=True)
    period03 = models.CharField(max_length=45, blank=True, null=True)
    period04 = models.CharField(max_length=45, blank=True, null=True)
    period05 = models.CharField(max_length=45, blank=True, null=True)
    period06 = models.CharField(max_length=45, blank=True, null=True)
    period07 = models.CharField(max_length=45, blank=True, null=True)
    period08 = models.CharField(max_length=45, blank=True, null=True)
    period09 = models.CharField(max_length=45, blank=True, null=True)
    period10 = models.CharField(max_length=45, blank=True, null=True)
    period11 = models.CharField(max_length=45, blank=True, null=True)
    period12 = models.CharField(max_length=45, blank=True, null=True)
    period13 = models.CharField(max_length=45, blank=True, null=True)
    period14 = models.CharField(max_length=45, blank=True, null=True)
    period15 = models.CharField(max_length=45, blank=True, null=True)
    period16 = models.CharField(max_length=45, blank=True, null=True)
    period17 = models.CharField(max_length=45, blank=True, null=True)
    period18 = models.CharField(max_length=45, blank=True, null=True)
    period19 = models.CharField(max_length=45, blank=True, null=True)
    period20 = models.CharField(max_length=45, blank=True, null=True)
    period21 = models.CharField(max_length=45, blank=True, null=True)
    period22 = models.CharField(max_length=45, blank=True, null=True)
    period23 = models.CharField(max_length=45, blank=True, null=True)
    period24 = models.CharField(max_length=45, blank=True, null=True)
    period25 = models.CharField(max_length=45, blank=True, null=True)
    period26 = models.CharField(max_length=45, blank=True, null=True)
    period27 = models.CharField(max_length=45, blank=True, null=True)
    period28 = models.CharField(max_length=45, blank=True, null=True)
    period29 = models.CharField(max_length=45, blank=True, null=True)
    period30 = models.CharField(max_length=45, blank=True, null=True)
    period31 = models.CharField(max_length=45, blank=True, null=True)
    total = models.CharField(max_length=45, blank=True, null=True)
    signature = models.CharField(max_length=45, blank=True, null=True)
    entrydatetime = models.DateTimeField(db_column='entryDatetime', blank=True, null=True)  # Field name made lowercase.
    temperatureunits = models.CharField(db_column='temperatureUnits', max_length=45, blank=True, null=True,
                                        choices=TEMP, default=DEG_C)  # Field name made lowercase.
    precipunits = models.CharField(db_column='precipUnits', max_length=45, blank=True, null=True,
                                   choices=PRECIP, default=MM)  # Field name made lowercase.
    cloudheightunits = models.CharField(db_column='cloudHeightUnits', max_length=45, blank=True, null=True,
                                        choices=CLOUD, default=FEET)  # Field name made lowercase.
    visunits = models.CharField(db_column='visUnits', max_length=45, blank=True, null=True,
                                choices=VIS, default=METRES)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'form_daily2'
        unique_together = (('stationid', 'elementid', 'yyyy', 'mm', 'hh'),)

    def get_absolute_url(self):
        return reverse('keyentry:form_daily2')


class FormMonthly(KeyEntryModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    stationid = models.CharField(db_column='stationId', max_length=255)  # Field name made lowercase.
    elementid = models.IntegerField(db_column='elementId')  # Field name made lowercase.
    yyyy = models.IntegerField()
    mm_01 = models.CharField(max_length=255, blank=True, null=True)
    mm_02 = models.CharField(max_length=255, blank=True, null=True)
    mm_03 = models.CharField(max_length=255, blank=True, null=True)
    mm_04 = models.CharField(max_length=255, blank=True, null=True)
    mm_05 = models.CharField(max_length=255, blank=True, null=True)
    mm_06 = models.CharField(max_length=255, blank=True, null=True)
    mm_07 = models.CharField(max_length=255, blank=True, null=True)
    mm_08 = models.CharField(max_length=255, blank=True, null=True)
    mm_09 = models.CharField(max_length=255, blank=True, null=True)
    mm_10 = models.CharField(max_length=255, blank=True, null=True)
    mm_11 = models.CharField(max_length=255, blank=True, null=True)
    mm_12 = models.CharField(max_length=255, blank=True, null=True)
    flag01 = models.CharField(max_length=255, blank=True, null=True, choices=FLAGS)
    flag02 = models.CharField(max_length=255, blank=True, null=True, choices=FLAGS)
    flag03 = models.CharField(max_length=255, blank=True, null=True, choices=FLAGS)
    flag04 = models.CharField(max_length=255, blank=True, null=True, choices=FLAGS)
    flag05 = models.CharField(max_length=255, blank=True, null=True, choices=FLAGS)
    flag06 = models.CharField(max_length=255, blank=True, null=True, choices=FLAGS)
    flag07 = models.CharField(max_length=255, blank=True, null=True, choices=FLAGS)
    flag08 = models.CharField(max_length=255, blank=True, null=True, choices=FLAGS)
    flag09 = models.CharField(max_length=255, blank=True, null=True, choices=FLAGS)
    flag10 = models.CharField(max_length=255, blank=True, null=True, choices=FLAGS)
    flag11 = models.CharField(max_length=255, blank=True, null=True, choices=FLAGS)
    flag12 = models.CharField(max_length=255, blank=True, null=True, choices=FLAGS)
    period01 = models.CharField(max_length=255, blank=True, null=True)
    period02 = models.CharField(max_length=255, blank=True, null=True)
    period03 = models.CharField(max_length=255, blank=True, null=True)
    period04 = models.CharField(max_length=255, blank=True, null=True)
    period05 = models.CharField(max_length=255, blank=True, null=True)
    period06 = models.CharField(max_length=255, blank=True, null=True)
    period07 = models.CharField(max_length=255, blank=True, null=True)
    period08 = models.CharField(max_length=255, blank=True, null=True)
    period09 = models.CharField(max_length=255, blank=True, null=True)
    period10 = models.CharField(max_length=255, blank=True, null=True)
    period11 = models.CharField(max_length=255, blank=True, null=True)
    period12 = models.CharField(max_length=255, blank=True, null=True)
    signature = models.CharField(max_length=50, blank=True, null=True)
    entrydatetime = models.DateTimeField(db_column='entryDatetime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'form_monthly'
        unique_together = (('stationid', 'elementid', 'yyyy'),)

    def get_absolute_url(self):
        return reverse('keyentry:form_monthly')


class FormSynoptic2Ra1(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    stationid = models.CharField(db_column='stationId', max_length=255)  # Field name made lowercase.
    yyyy = models.IntegerField()
    mm = models.IntegerField()
    dd = models.IntegerField()
    hh = models.IntegerField()
    val_elem106 = models.CharField(db_column='Val_Elem106', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem107 = models.CharField(db_column='Val_Elem107', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem400 = models.CharField(db_column='Val_Elem400', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem814 = models.CharField(db_column='Val_Elem814', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem399 = models.CharField(db_column='Val_Elem399', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem301 = models.CharField(db_column='Val_Elem301', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem185 = models.CharField(db_column='Val_Elem185', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem101 = models.CharField(db_column='Val_Elem101', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem102 = models.CharField(db_column='Val_Elem102', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem103 = models.CharField(db_column='Val_Elem103', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem105 = models.CharField(db_column='Val_Elem105', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem192 = models.CharField(db_column='Val_Elem192', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem110 = models.CharField(db_column='Val_Elem110', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem114 = models.CharField(db_column='Val_Elem114', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem112 = models.CharField(db_column='Val_Elem112', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem111 = models.CharField(db_column='Val_Elem111', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem167 = models.CharField(db_column='Val_Elem167', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem197 = models.CharField(db_column='Val_Elem197', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem193 = models.CharField(db_column='Val_Elem193', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem115 = models.CharField(db_column='Val_Elem115', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem168 = models.CharField(db_column='Val_Elem168', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem169 = models.CharField(db_column='Val_Elem169', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem170 = models.CharField(db_column='Val_Elem170', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem171 = models.CharField(db_column='Val_Elem171', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem119 = models.CharField(db_column='Val_Elem119', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem116 = models.CharField(db_column='Val_Elem116', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem117 = models.CharField(db_column='Val_Elem117', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem118 = models.CharField(db_column='Val_Elem118', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem123 = models.CharField(db_column='Val_Elem123', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem120 = models.CharField(db_column='Val_Elem120', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem121 = models.CharField(db_column='Val_Elem121', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem122 = models.CharField(db_column='Val_Elem122', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem127 = models.CharField(db_column='Val_Elem127', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem124 = models.CharField(db_column='Val_Elem124', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem125 = models.CharField(db_column='Val_Elem125', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem126 = models.CharField(db_column='Val_Elem126', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem131 = models.CharField(db_column='Val_Elem131', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem128 = models.CharField(db_column='Val_Elem128', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem129 = models.CharField(db_column='Val_Elem129', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem130 = models.CharField(db_column='Val_Elem130', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem002 = models.CharField(db_column='Val_Elem002', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem003 = models.CharField(db_column='Val_Elem003', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem099 = models.CharField(db_column='Val_Elem099', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem018 = models.CharField(db_column='Val_Elem018', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem084 = models.CharField(db_column='Val_Elem084', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem132 = models.CharField(db_column='Val_Elem132', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem005 = models.CharField(db_column='Val_Elem005', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem174 = models.CharField(db_column='Val_Elem174', max_length=6, blank=True, null=True)  # Field name made lowercase.
    val_elem046 = models.CharField(db_column='Val_Elem046', max_length=6, blank=True, null=True)  # Field name made lowercase.
    flag106 = models.CharField(db_column='Flag106', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag107 = models.CharField(db_column='Flag107', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag400 = models.CharField(db_column='Flag400', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag814 = models.CharField(db_column='Flag814', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag399 = models.CharField(db_column='Flag399', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag301 = models.CharField(db_column='Flag301', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag185 = models.CharField(db_column='Flag185', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag101 = models.CharField(db_column='Flag101', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag102 = models.CharField(db_column='Flag102', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag103 = models.CharField(db_column='Flag103', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag105 = models.CharField(db_column='Flag105', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag192 = models.CharField(db_column='Flag192', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag110 = models.CharField(db_column='Flag110', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag114 = models.CharField(db_column='Flag114', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag112 = models.CharField(db_column='Flag112', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag111 = models.CharField(db_column='Flag111', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag167 = models.CharField(db_column='Flag167', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag197 = models.CharField(db_column='Flag197', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag193 = models.CharField(db_column='Flag193', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag115 = models.CharField(db_column='Flag115', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag168 = models.CharField(db_column='Flag168', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag169 = models.CharField(db_column='Flag169', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag170 = models.CharField(db_column='Flag170', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag171 = models.CharField(db_column='Flag171', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag119 = models.CharField(db_column='Flag119', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag116 = models.CharField(db_column='Flag116', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag117 = models.CharField(db_column='Flag117', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag118 = models.CharField(db_column='Flag118', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag123 = models.CharField(db_column='Flag123', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag120 = models.CharField(db_column='Flag120', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag121 = models.CharField(db_column='Flag121', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag122 = models.CharField(db_column='Flag122', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag127 = models.CharField(db_column='Flag127', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag124 = models.CharField(db_column='Flag124', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag125 = models.CharField(db_column='Flag125', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag126 = models.CharField(db_column='Flag126', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag131 = models.CharField(db_column='Flag131', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag128 = models.CharField(db_column='Flag128', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag129 = models.CharField(db_column='Flag129', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag130 = models.CharField(db_column='Flag130', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag002 = models.CharField(db_column='Flag002', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag003 = models.CharField(db_column='Flag003', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag099 = models.CharField(db_column='Flag099', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag018 = models.CharField(db_column='Flag018', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag084 = models.CharField(db_column='Flag084', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag132 = models.CharField(db_column='Flag132', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag005 = models.CharField(db_column='Flag005', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag174 = models.CharField(db_column='Flag174', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag046 = models.CharField(db_column='Flag046', max_length=1, blank=True, null=True)  # Field name made lowercase.
    signature = models.CharField(max_length=45, blank=True, null=True)
    entrydatetime = models.DateTimeField(db_column='entryDatetime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'form_synoptic_2_ra1'
        unique_together = (('stationid', 'yyyy', 'mm', 'dd', 'hh'),)

    def get_absolute_url(self):
        return reverse('keyentry:form_synoptic2ra1')
