import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker

from app.models import Client, Parking
from app.app import db

fake = Faker("ru_RU")


class ClientFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")

    credit_card = factory.Maybe(
        factory.Faker("boolean"),
        yes_declaration=factory.Faker("credit_card_number"),
        no_declaration=None
    )

    car_number = factory.Faker("bothify", text="?#?###")


class ParkingFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    address = factory.Faker("address")
    opened = factory.Faker("boolean")
    count_places = factory.Faker("random_int", min=5, max=50)

    count_available_places = factory.LazyAttribute(
        lambda p: p.count_places
    )
