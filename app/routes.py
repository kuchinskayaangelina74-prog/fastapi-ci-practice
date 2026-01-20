from flask import Blueprint, request, jsonify
from .models import Client, Parking, ClientParking
from .app import db
from datetime import datetime

api = Blueprint("api", __name__)

@api.route("/clients", methods=["GET"])
def get_clients():
    clients = Client.query.all()
    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "surname": c.surname,
            "car_number": c.car_number
        } for c in clients
    ])


@api.route("/clients/<int:client_id>", methods=["GET"])
def get_client(client_id):
    client = Client.query.get_or_404(client_id)

    return jsonify({
        "id": client.id,
        "name": client.name,
        "surname": client.surname,
        "credit_card": client.credit_card,
        "car_number": client.car_number
    })


@api.route("/clients", methods=["POST"])
def create_client():
    data = request.json

    client = Client(
        name=data["name"],
        surname=data["surname"],
        credit_card=data.get("credit_card"),
        car_number=data.get("car_number")
    )

    db.session.add(client)
    db.session.commit()

    return jsonify({"message": "Client created", "id": client.id}), 201


@api.route("/parkings", methods=["POST"])
def create_parking():
    data = request.json

    parking = Parking(
        address=data["address"],
        opened=data.get("opened", True),
        count_places=data["count_places"],
        count_available_places=data["count_places"]
    )

    db.session.add(parking)
    db.session.commit()

    return jsonify({"message": "Parking created", "id": parking.id}), 201


@api.route("/parkings", methods=["GET"])
def get_parkings():
    parkings = Parking.query.all()
    return jsonify([
        {
            "id": p.id,
            "address": p.address,
            "opened": p.opened,
            "count_places": p.count_places,
            "count_available_places": p.count_available_places,
        }
        for p in parkings
    ])


@api.route("/parkings/<int:parking_id>", methods=["GET"])
def get_parking(parking_id):
    parking = Parking.query.get_or_404(parking_id)

    return jsonify({
        "id": parking.id,
        "address": parking.address,
        "opened": parking.opened,
        "count_places": parking.count_places,
        "count_available_places": parking.count_available_places,
    })


@api.route("/client_parkings", methods=["POST"])
def enter_parking():
    data = request.json

    client = Client.query.get_or_404(data["client_id"])
    parking = Parking.query.get_or_404(data["parking_id"])

    if not parking.opened:
        return jsonify({"error": "Parking is closed"}), 400

    if parking.count_available_places <= 0:
        return jsonify({"error": "No available places"}), 400

    log = ClientParking(
        client_id=client.id,
        parking_id=parking.id,
        time_in=datetime.utcnow()
    )

    parking.count_available_places -= 1

    db.session.add(log)
    db.session.commit()

    return jsonify({"message": "Car entered parking"})


@api.route("/client_parkings", methods=["DELETE"])
def exit_parking():
    data = request.json

    log = ClientParking.query.filter_by(
        client_id=data["client_id"],
        parking_id=data["parking_id"],
        time_out=None
    ).first_or_404()

    client = Client.query.get(log.client_id)
    parking = Parking.query.get(log.parking_id)

    if not client.credit_card:
        return jsonify({"error": "No credit card"}), 400

    log.time_out = datetime.utcnow()
    parking.count_available_places += 1

    db.session.commit()

    return jsonify({"message": "Car exited parking, payment successful"})
