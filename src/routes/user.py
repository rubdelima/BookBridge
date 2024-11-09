from flask import Blueprint, request, jsonify
from src.database.models import db, Usuario
from src.database import model_validation as validator

users_bp = Blueprint('usuarios', __name__)

@users_bp.route('/usuarios', methods=['POST'])
def post_user():
    # Validação dos campos do Usuário
    user = validator.valide_user(request.json)
    
    try:
        # Salva o novo usuário no banco de dados
        db.session.add(user)
        db.session.commit()
        return jsonify(user.id), 201
    
    except Exception as e:
        # Desfaz alteracões e retorna o erro
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
