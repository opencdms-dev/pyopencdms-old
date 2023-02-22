"""
Running these tests requires pygeoapi server
(configured with climsoft pygeoapi provider) running
"""
import requests
import random
import datetime
import uuid
import faker

fake = faker.Faker()
BASE_URL = "http://localhost:5000"
INSERT_DATA = dict(
    recordedFrom="67774010",
    describedBy=4,
    obsDatetime=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
    qcStatus=random.randint(1, 10),
    acquisitionType=random.randint(1, 10),
    obsLevel=uuid.uuid4().hex,
    obsValue=100,
    flag=uuid.uuid4().hex,
    period=random.choice([10, 100, 1000]),
    qcTypeLog=fake.sentence(),
    dataForm=uuid.uuid4().hex,
    capturedBy=uuid.uuid4().hex,
    mark=True,
    temperatureUnits=uuid.uuid4().hex,
    precipitationUnits=uuid.uuid4().hex,
    cloudHeightUnits=uuid.uuid4().hex,
    visUnits=uuid.uuid4().hex,
    dataSourceTimeZone=random.randint(1, 180),
)

UPDATE_DATA = {"flag": "abcd"}


def test_should_create_query_get_update_and_delete_record_sequentially():
    # create
    response = requests.post(
        url=f"{BASE_URL}/collections/climsoft/items",
        json=INSERT_DATA,
        headers={"Content-Type": "application/geo+json"},
    )

    assert response.status_code == 201

    # query
    response = requests.get(
        url=f"{BASE_URL}/collections/climsoft/items",
        headers={"Content-Type": "application/geo+json"},
    )

    assert type(response.json()["features"]) == list

    # get
    response = requests.get(
        url=f"{BASE_URL}/collections/climsoft"
            f"/items/67774010*4*{INSERT_DATA['obsDatetime']}",
        headers={"Content-Type": "application/geo+json"},
    )

    assert response.status_code == 200

    # update
    response = requests.put(
        url=f"{BASE_URL}/collections/climsoft"
            f"/items/67774010*4*{INSERT_DATA['obsDatetime']}",
        headers={"Content-Type": "application/geo+json"},
        json=UPDATE_DATA,
    )

    assert response.status_code == 204

    # delete
    response = requests.delete(
        url=f"{BASE_URL}/collections/climsoft"
            f"/items/67774010*4*{INSERT_DATA['obsDatetime']}",
        headers={"Content-Type": "application/geo+json"},
    )

    assert response.status_code == 200
