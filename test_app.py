import pytest
from app import app, db


@pytest.fixture
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client


def test_empty_db(client):
    rv = client.get('/measurements/latest')
    assert rv.json == {"measurements": []}
