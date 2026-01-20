import pytest

from app.app import create_app, db
from app.models import Client, Parking


@pytest.fixture
def app():
    app = create_app()
    app.config.update(
        {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"}
    )

    with app.app_context():
        db.create_all()

        client = Client(
            name="Test",
            surname="User",
            credit_card="1111-2222-3333-4444",
            car_number="A123BC",
        )

        parking = Parking(
            address="Test street",
            opened=True,
            count_places=10,
            count_available_places=10,
        )

        db.session.add_all([client, parking])
        db.session.commit()

        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db_session(app):
    return db
