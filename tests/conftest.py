import pytest
from src.app import create_app
from src.database.models import db

@pytest.fixture(scope='module')
def setup_database():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()
        yield db 
        db.drop_all()

@pytest.fixture
def client(setup_database):
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client, app.app_context():
        yield client 
