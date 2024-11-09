from flask import Blueprint, request, jsonify
from src.database.models import db, Usuario
from src.database import model_validation as validator, autenticar

users_bp = Blueprint('usuarios', __name__)

@users_bp.route('/usuarios', methods=['POST'])
def post_user():
    """
    Endpoint para criação de um novo usuário.
    
    Parâmetros de Entrada:
        - email : str (email do novo usuário)
        - senha : str (senha do novo usuário)
        - nickname : str (nickname do novo usuário)
        - nome : str (nome do novo usuário)
        - sobrenome : str (sobrenome do novo usuário)
    
    Retorno:
        - 201 : Created - Se o usuário foi criado com sucesso
        - 401 : Invalid - Se já houver um outro usuário já cadastrado com o mesmo nickname ou email
        - 403 : Forbidden - Se algum campo não foi preenchido, ou foi preenchido incorretamente
        - 500 : Internal Server Error - Se houve algum erro durante a criação do usuário
    """
        
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
    
@users_bp.route('/usuarios/login/', methods=['GET'])
def login_user():
    """
    Endpoint para login de um usuário.
    
    Parâmetros de Entrada:
        - email : Optional[str] (email do usuário)
        - nickname : Optional[str] (nickname do usuário)
        - senha : str (senha do usuário)
    
    Retorno:
        - 200 : OK - Se o login foi realizado com sucesso
        - 401 : Unauthorized - Se o email, nickname ou senha estão incorretos
        - 500 : Internal Server Error - Se houve algum erro durante o login
    """
    
    dados = request.json
    
    try:
        assert (senha:= dados.get('senha'))
    except:
        return jsonify(
            {"error" : "O campo de senha não foi preenchido"}
        ), 403
    
    try:
        assert (email := dados.get('email')) or (nickname := dados.get('nickname'))
    except:
        return jsonify(
            {"error" : "O campo de email ou nickname não foi preenchido"}
        ), 403
    
    try:
        user = autenticar(email=email, nickname=nickname, senha=senha)
    except:
        return jsonify(
            {"error" : "Email, nickname ou senha incorretos"}
        ), 401
    
    return jsonify(user.id), 200
    

@users_bp.route('/usuarios', methods=['GET'])
def get_user():
    
    
    user_id = request.json.get('user_id')
    
    # Busca o user no banco de dados
    user = Usuario.query.filter_by(id = user_id)
    
    # Retorna o usuário caso exista
    if user.first():
        return jsonify(user.first().to_dict()), 200
    
    # Caso não exista, retorna um erro
    return jsonify({"error": "Usuário não encontrado"}), 404

