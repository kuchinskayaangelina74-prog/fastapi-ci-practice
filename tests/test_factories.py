from app.models import Client, Parking
from tests.factories import ClientFactory, ParkingFactory


def test_create_client_with_factory(db_session):
    clients_before = Client.query.count()

    client = ClientFactory()

    clients_after = Client.query.count()

    assert client.id is not None
    assert clients_after == clients_before + 1


def test_create_parking_with_factory(db_session):
    parkings_before = Parking.query.count()

    parking = ParkingFactory()

    parkings_after = Parking.query.count()

    assert parking.id is not None
    assert parking.count_available_places == parking.count_places
    assert parkings_after == parkings_before + 1
