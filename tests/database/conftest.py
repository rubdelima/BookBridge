import pytest
from src.app import create_app
from src.database.models import db

@pytest.fixture(scope='module')
def setup_database():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Banco de dados em memória para testes
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():  # Garante que o contexto da aplicação esteja ativo
        db.create_all()  # Cria as tabelas no banco de dados de teste
        yield db
        db.drop_all()  # Limpa as tabelas após os testes

@pytest.fixture
def client(setup_database):
    app = create_app()
    with app.test_client() as client, app.app_context():  # Garante que o contexto esteja ativo para cada teste
        yield client
