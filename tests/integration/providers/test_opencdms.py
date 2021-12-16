from opencdms.provider.opencdms import OpenCDMSProvider, ProviderConfig
from tests.unit.dtos.data import station_data
from opencdms.models import clide


def test_clide_provider():
    provider = OpenCDMSProvider(ProviderConfig(enable_clide=True))

    station = provider.create("Station", station_data)
    assert isinstance(station["clide"], clide.Station)

    station = provider.get("Station", {"id": station_data["id"]})
    assert isinstance(station["clide"], clide.Station)

    stations = provider.list("Station")
    for station in stations["clide"]:
        assert isinstance(station, clide.Station)

    station = provider.update(
        "Station",
        {"id": station_data["id"]},
        {'region': 'US'}
    )

    assert station["clide"].region == 'US'

    deleted = provider.delete(
        "Station",
        {"id": station_data['id']}
    )

    assert deleted["clide"] == {"id": station_data['id']}
