import pytest


@pytest.mark.parametrize(
    "url",
    [
        "/clients",
        "/clients/1",
        "/parkings",
        "/parkings/1",
    ]
)
def test_get_methods(client, url):
    response = client.get(url)
    assert response.status_code == 200


def test_create_client(client):
    response = client.post(
        "/clients",
        json={
            "name": "Ivan",
            "surname": "Ivanov",
            "credit_card": "9999-8888-7777-6666",
            "car_number": "B777BB"
        }
    )

    assert response.status_code == 201
    assert response.json["message"] == "Client created"


def test_create_parking(client):
    response = client.post(
        "/parkings",
        json={
            "address": "New parking",
            "count_places": 5
        }
    )

    assert response.status_code == 201
    assert response.json["message"] == "Parking created"


@pytest.mark.parking
def test_enter_parking(client):
    response = client.post(
        "/client_parkings",
        json={
            "client_id": 1,
            "parking_id": 1
        }
    )

    assert response.status_code == 200
    assert response.json["message"] == "Car entered parking"


@pytest.mark.parking
def test_exit_parking(client):
    enter_response = client.post(
        "/client_parkings",
        json={
            "client_id": 1,
            "parking_id": 1
        }
    )
    assert enter_response.status_code == 200

    exit_response = client.delete(
        "/client_parkings",
        json={
            "client_id": 1,
            "parking_id": 1
        }
    )

    assert exit_response.status_code == 200
    assert "payment successful" in exit_response.json["message"]
