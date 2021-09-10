import os
import django
from django.conf import settings
from django.core.management import execute_from_command_line

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def setup_module(module):
    try:
        settings.configure(
            DATABASES={
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": os.path.join(BASE_DIR, "tests/db.sqlite3"),
                }
            },
            DEFAULT_AUTO_FIELD="django.db.models.AutoField",
            BASE_DIR=BASE_DIR,
            INSTALLED_APPS=(
                "opencdms.models.djangodemo",
                "django.contrib.auth",
                "django.contrib.contenttypes"
            )
        )
    except RuntimeError:
        pass

    django.setup()

    execute_from_command_line([
        os.path.abspath(__file__),
        "makemigrations",
        "djangodemo"
    ])
    execute_from_command_line([
        os.path.abspath(__file__),
        "migrate"
    ])


def teardown_module(module):
    os.remove(os.path.join(BASE_DIR, "tests/db.sqlite3"))


def test_should_return_same_station_ids():
    from opencdms.models.djangodemo.metadata import Station

    station_ids = ['838', '675']

    for st_id in station_ids:
        new_station = Station(
            stationid=st_id,
            stationname='BRACKNELL: BEAUFORT PARK',
            latitude=51.3898,
            longitude=-0.784,
            openingdatetime='1965-01-01',
            closingdatetime='2003-06-30',
            country='UK',
            authority='Met Office',
            stationoperational=False,
        )
        new_station.save()

    for st in Station.objects.all():
        assert st.stationid in station_ids
