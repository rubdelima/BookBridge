# Flask Libs
from flask_caching import Cache
from flask import Flask
from flasgger import Swagger

# BluePrints
from src.routes.books import books_bp
from src.routes.club_books import club_books_bp
from src.routes.clubs import clubs_bp
from src.routes.user import users_bp
from src.routes.user_club import user_club_bp

# Database
from src.database.models import db

# Externals Libraries
import logging

def create_app():
    app = Flask(__name__)
    
    # Adicionando os BluePrints
    app.register_blueprint(books_bp)
    app.register_blueprint(club_books_bp)
    app.register_blueprint(clubs_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(user_club_bp)
    
    # Iniciando o Swagger
    Swagger(app)
    
    # Configuração do banco de dados    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Configurando a chave de decodificaçao JWT
    app.config['SECRET_KEY'] = '936eb4f154867b74386f1bfc930ae0e7e8e4f9a759557dbfce0cb9f3a4a49edf'
    
    # Configuração do Logger
    file_handler = logging.FileHandler('./app.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(f'%(asctime)s - %(levelname)-{6}s : %(message)s'))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.DEBUG)
    app.logger.info(f"API BookBridge Iniciada")
    
    # Configuração do Cache
    cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
    cache.init_app(app)
    
    app.logger.info("Sistema de Cache Inicializado")
    
    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
