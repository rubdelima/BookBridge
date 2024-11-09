from flask import Blueprint, request, jsonify
from src.database.models import db, Usuario
from src.database import model_validation as validator, autenticar

users_bp = Blueprint('usuarios', __name__)

@users_bp.route('/usuarios', methods=['POST'])
def post_user():
    """
    ## Endpoint para criação de um novo usuário.
    
    ### Parâmetros de Entrada:
    
    - email : str (email do novo usuário)
    
    - senha : str (senha do novo usuário)
    
    - nickname : str (nickname do novo usuário)
    
    - nome : str (nome do novo usuário)
    
    - sobrenome : str (sobrenome do novo usuário)
    
    
    ### Retorno:
    
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
        return jsonify({'token' : validator.get_token(user.id)}), 200
    
    except Exception as e:
        # Desfaz alteracões e retorna o erro
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
@users_bp.route('/usuarios/login/', methods=['GET'])
def login_user():
    """
    ## Endpoint para login de um usuário.
    
    ### Parâmetros de Entrada:
    - email : Optional[str] (email do usuário)
        
    - nickname : Optional[str] (nickname do usuário)
        
    - senha : str (senha do usuário)
        
    
    ### Códigos de Retorno:
    - 200 : OK - Se o login foi realizado com sucesso
        
    - 401 : Unauthorized - Se o email, nickname ou senha estão incorretos
        
    - 500 : Internal Server Error - Se houve algum erro durante o login
        
    
    ### Retono:
    - token : str (token de autenticação)
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
    
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({'token' : validator.get_token(user.id)}), 200
    except:
        db.session.rollback()
        return jsonify({"error": "Ocorreu um erro durante o login"}), 500
    
    

@users_bp.route('/usuarios', methods=['GET'])
@validator.check_jwt_token
def get_user(current_user):
    """
    Endpoint para listar os dados do usuário logado.
    
    Parâmetros de Entrada:
        - token : str (token de autenticação) Deve ser enviado no header de Authorization
    
    Retorno:
        - 200 : OK - Se os dados do usuário foram retornados com sucesso
        - 401 : Not authorized - Se o token de autenticação está espirado
        - 403 : Forbidden - Se o token de autenticação não é válido
        - 500 : Internal Server Error - Se houve algum erro durante a listagem dos dados
    """
    try:
        return jsonify(current_user.to_dict()), 200
    except:
        return jsonify({"error": "Ocorreu um erro durante a listagem dos dados"}), 500

@users_bp.route('/usuarios', methods=['PUT'])
@validator.check_jwt_token
def update_user(current_user):
    """
    Endpoint para atualizar os dados do usuário logado.
    
    Parâmetros de Entrada:
        - token : str (token de autenticação) Deve ser enviado no header de Authorization
        - email : Optional[str] (email do novo usuário)
        - senha : Optional[str] (senha do novo usuário)
        - nickname : Optional[str] (nickname do novo usuário)
        - nome : Optional[str] (nome do novo usuário)
        - sobrenome : Optional[str] (sobrenome do novo usuário)
    
    Retorno:
    - 200 : OK - Se os dados do usuário foram atualizados com sucesso
    - 401 : Not authorized - Se o token de autenticação está espirado
    - 403 : Forbidden - Se o token de autenticação não é válido
    - 500 : Internal Server Error - Se houve algum erro durante a atualização dos dados
    """
    
    dados = request.json
    
    updated_user_json = {
        'id': current_user.id,  # Mantém o ID atual do usuário
        'email': dados.get('email', current_user.email),
        'senha': dados.get('senha', current_user.senha),
        'nickname': dados.get('nickname', current_user.nickname),
        'nome': dados.get('nome', current_user.nome),
        'sobrenome': dados.get('sobrenome', current_user.sobrenome)
    }
    
    updated_user = validator.valide_user(updated_user_json)
    
    update_user.email = updated_user.email
    update_user.senha = updated_user.senha
    update_user.nickname = updated_user.nickname
    update_user.nome = updated_user.nome
    update_user.sobrenome = updated_user.sobrenome
    
    try:
        db.session.commit()
        return jsonify({'message': 'Usuário atualizado com sucesso'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@users_bp.route('/usuarios', methods=['DELETE'])
@validator.check_jwt_token
def delete_user(current_user):
    """
    ## Endpoint para a exclusão de um usuario
    
    Parâmetros de Entrada:
        - token : str (token de autenticação) Deve ser enviado no header de Authorization
    
    Retorno:
    - 200 : OK - Se o usuário foi excluído com sucesso
    - 401 : Not authorized - Se o token de autenticação está espirado
    - 403 : Forbidden - Se o token de autenticação não é válido
    - 500 : Internal Server Error - Se houve algum erro durante a exclusão do usuário
    """
    try:
        db.session.delete(current_user)
        db.session.commit()
        return jsonify({'message': 'Usuário excluído com sucesso'}), 200
    except:
        db.session.rollback()
        return jsonify({"error": "Não foi possível excluir o usuário"}), 500
    
    
@users_bp.route('/usuarios/<nickname>', methods=['GET'])
@validator.check_jwt_token
def get_user_by_nickname(current_user, nickname):
    """
    Endpoint para buscar um usuário pelo nickname.
    
    Parâmetros de Entrada:
        - token : str (token de autenticação) Deve ser enviado no header de Authorization
        - nickname : str (nickname do usuário)
    
    Retorno:
    - 200 : OK - Se o usuário foi encontrado com sucesso
    - 401 : Not authorized - Se o token de autenticação está espirado
    - 403 : Forbidden - Se o token de autenticação não é válido
    - 404 : Not Found - Se o usuário não foi encontrado
    - 500 : Internal Server Error - Se houve algum erro durante a busca do usuário
    """
    
    user = Usuario.query.filter_by(nickname=nickname).first()
    
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404
    
    return jsonify(user.to_dict()), 200