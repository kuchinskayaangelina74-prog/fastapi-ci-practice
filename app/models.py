from datetime import datetime

from .app import db


class Client(db.Model):
    __tablename__ = "client"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.String(50), nullable=True)
    car_number = db.Column(db.String(10), nullable=True)

    parking_logs = db.relationship(
        "ClientParking", backref="client", lazy=True
        )

    def __repr__(self):
        return f"<Client {self.name} {self.surname} ({self.car_number})>"


class Parking(db.Model):
    __tablename__ = "parking"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    opened = db.Column(db.Boolean, nullable=True)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)

    client_logs = db.relationship("ClientParking", backref="parking", lazy=True)

    def __repr__(self):
        return f"<Parking {self.address} ({self.count_available_places}/{self.count_places})>"


class ClientParking(db.Model):
    __tablename__ = "client_parking"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=True)
    parking_id = db.Column(db.Integer, db.ForeignKey("parking.id"), nullable=True)
    time_in = db.Column(db.DateTime, nullable=True)
    time_out = db.Column(db.DateTime, nullable=True)

    __table_args__ = (
        db.UniqueConstraint("client_id", "parking_id", name="unique_client_parking"),
    )

    def __repr__(self):
        return (
            f"<ClientParking client_id={self.client_id} parking_id={self.parking_id}>"
        )
