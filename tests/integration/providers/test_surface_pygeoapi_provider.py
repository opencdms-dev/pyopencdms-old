"""
Running these tests requires pygeoapi server
(configured with surface pygeoapi provider) running
"""
import requests
import datetime
import faker

fake = faker.Faker()
BASE_URL = "http://localhost:5000"
INSERT_DATA = dict(
    station_id=14,
    variable_id=34,
    datetime=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
    measured=100,
    consisted=100,
    quality_flag=4,
    observation_flag_id=2
)

UPDATE_DATA = {"code": "abcd"}


def test_should_create_query_get_update_and_delete_record_sequentially():
    # create
    response = requests.post(
        url=f"{BASE_URL}/collections/surface/items",
        json=INSERT_DATA,
        headers={"Content-Type": "application/geo+json"},
    )

    assert response.status_code == 201

    # query
    response = requests.get(
        url=f"{BASE_URL}/collections/surface/items",
        headers={"Content-Type": "application/geo+json"},
    )

    assert type(response.json()["features"]) == list

    # get
    response = requests.get(
        url=f"{BASE_URL}/collections/surface"
            f"/items/14*34*{INSERT_DATA['datetime']}",
        headers={"Content-Type": "application/geo+json"},
    )

    assert response.status_code == 200

    # update
    response = requests.put(
        url=f"{BASE_URL}/collections/surface"
            f"/items/14*34*{INSERT_DATA['datetime']}",
        headers={"Content-Type": "application/geo+json"},
        json=UPDATE_DATA,
    )

    assert response.status_code == 204

    # delete
    response = requests.delete(
        url=f"{BASE_URL}/collections/surface"
            f"/items/14*34*{INSERT_DATA['datetime']}",
        headers={"Content-Type": "application/geo+json"},
    )

    assert response.status_code == 200
