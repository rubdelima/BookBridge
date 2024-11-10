from flask import Flask
from src.database.models import db
from src.routes.user import users_bp
# from src.routes.books import books_bp
import logging
from datetime import datetime, timezone


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '936eb4f154867b74386f1bfc930ae0e7e8e4f9a759557dbfce0cb9f3a4a49edf'

    db.init_app(app)

    app.register_blueprint(users_bp)
    # app.register_blueprint(books_bp)
    
    # Configuração do Logger
    file_handler = logging.FileHandler('./app.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(f'%(asctime)s - %(levelname)-{6}s : %(message)s'))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.DEBUG)
    app.logger.info(f"API BookBridge Iniciada")
    
    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
