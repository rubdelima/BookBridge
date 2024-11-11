import pytest
from src.app import create_app
from src.database.models import db
from sqlalchemy.sql import text

@pytest.fixture(scope='session')
def setup_database():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()
        
        app.logger.info("Povoando banco de dados com dados locais")
        try:
            with open('./src/database/populate_tables.sql') as f:
                sql_statements = f.read()
                for statement in sql_statements.split(';'):
                    if statement.strip():
                        db.session.execute(text(statement))
                db.session.commit()
            app.logger.info("Banco de dados com dados locais populado com sucesso")
            
        except Exception as e:
            app.logger.error(f"Erro ao carregar dados de teste: {e}")
            db.session.rollback()
            raise e
        
        yield app 
        db.drop_all()

@pytest.fixture
def client(setup_database):
    with setup_database.test_client() as client:
        yield client
