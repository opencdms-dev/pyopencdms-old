import datetime
import uuid
import random
import pytest
from sqlalchemy import create_engine
from sqlalchemy.sql import text as sa_text
from sqlalchemy.orm import sessionmaker
from opencdms.models.midas import core as midas_models
from test_util import get_midas_connection_string

DB_URL = get_midas_connection_string()


db_engine = create_engine(DB_URL)

equipment_data = dict(
    equipment_id=random.randint(1, 10000),
    equipment_type_id=random.randint(1, 10000),
    manufacturer_name=uuid.uuid4().hex[:28],
    manufacturer_sn_txt=uuid.uuid4().hex[:28],
    met_ref_txt=uuid.uuid4().hex[:28],
    eqpt_prct_date=datetime.datetime.utcnow().strftime("%Y:%m:%d %H:%M:%S"),
    equipment_cost=random.random()*10000,
    eqpt_dspl_date=datetime.datetime.utcnow().strftime("%Y:%m:%d %H:%M:%S"),
    eqpt_dspl_rmrk=uuid.uuid4().hex,
    eqpt_last_updated_date=datetime.datetime.utcnow().strftime(
        "%Y:%m:%d %H:%M:%S"
    )
)


@pytest.fixture
def db_session():
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.close()


def setup_module(module):
    # Postgresql does not automatically reset ID
    # if a table is truncated like mysql does
    midas_models.Base.metadata.create_all(bind=db_engine)

    with db_engine.connect() as connection:
        with connection.begin():
            db_engine.execute(
                sa_text(
                    f'''
                    TRUNCATE TABLE {midas_models.Equipment.__tablename__}
                    RESTART IDENTITY CASCADE
                    '''
                ).execution_options(autocommit=True)
            )

    Session = sessionmaker(bind=db_engine)
    session = Session()

    session.add(midas_models.Equipment(**equipment_data))

    session.commit()
    session.close()


def teardown_module(module):
    # Postgresql does not automatically reset ID
    # if a table is truncated like mysql does
    midas_models.Base.metadata.create_all(bind=db_engine)

    with db_engine.connect() as connection:
        with connection.begin():
            db_engine.execute(
                sa_text(
                    f'''TRUNCATE TABLE {midas_models.Equipment.__tablename__}
                     RESTART IDENTITY CASCADE'''
                ).execution_options(autocommit=True)
            )


@pytest.mark.order(100)
def test_should_create_a_equipment(db_session):
    equipment = midas_models.Equipment(**equipment_data)
    db_session.add(equipment)
    db_session.commit()

    assert equipment.equipment_id == equipment_data['equipment_id']


@pytest.mark.order(101)
def test_should_read_all_equipments(db_session):
    equipments = db_session.query(midas_models.Equipment).all()

    for equipment in equipments:
        assert isinstance(equipment, midas_models.Equipment)


@pytest.mark.order(102)
def test_should_return_a_single_equipment(db_session):
    equipment = db_session.query(midas_models.Equipment)\
        .get(equipment_data['equipment_id'])

    assert equipment.equipment_id == equipment_data['equipment_id']


@pytest.mark.order(103)
def test_should_update_equipment(db_session):
    db_session.query(midas_models.Equipment)\
        .filter_by(equipment_id=equipment_data['equipment_id'])\
        .update({'region': 'US'})
    db_session.commit()

    updated_equipment = db_session.query(midas_models.Equipment)\
        .get(equipment_data['equipment_id'])

    assert updated_equipment.region == 'US'


@pytest.mark.order(104)
def test_should_delete_equipment(db_session):
    db_session.query(midas_models.Equipment)\
        .filter_by(equipment_id=equipment_data['equipment_id']).delete()
    db_session.commit()

    deleted_equipment = db_session.query(midas_models.Equipment)\
        .get(equipment_data['equipment_id'])

    assert deleted_equipment is None
