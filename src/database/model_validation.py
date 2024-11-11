from src.database.models import Usuario
from flask import jsonify
import re
import secrets
import jwt
from functools import wraps
from flask import request, jsonify, current_app
from datetime import datetime, timedelta, timezone

def check_jwt_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if (not token) or not(token.startswith('Bearer ')):
            current_app.logger.error('Token de autenticação é necessário')
            return jsonify({'message': 'Token de autenticação é necessário'}), 403

        try:
            data = jwt.decode(token.split(' ')[1], current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = Usuario.query.filter_by(id=data['user_id']).first()
        except jwt.ExpiredSignatureError:
            current_app.logger.error('Token expirado')
            return jsonify({'message': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            current_app.logger.error('Token invalido')
            return jsonify({'message': 'Token inválido'}), 401

        current_app.logger.info(f"Usuário {current_user.id} logado com sucesso! ")
        return f(current_user, *args, **kwargs)

    return decorated

def get_token(user_id):
    return jwt.encode({
        'user_id': user_id,
        'exp': datetime.now(tz=timezone.utc) + timedelta(days=7)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')

def valide_user(dados:dict)->Usuario:
    # Verificação se todos os campos foram preenchidos
    try:
        assert (user_email := dados.get('email')), ('email', )
        assert (senha := dados.get('senha')), ('senha', )
        assert (nickname := dados.get('nickname')), ('nickname', )
        assert (nome := dados.get('nome')), ('nome', )
        assert (sobrenome := dados.get('sobrenome'))
        
    except AssertionError as ae:
        current_app.logger.error(f"Campo de {ae.args[0]} não foi preenchido")
        return jsonify(
            {"error" : f"O campo de {ae.args[0]} não foi preenchido"}
        ), 403
    
    # Verificação do pattern do email
    try:
        assert re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', user_email)
    except:
        current_app.logger.error("Formato de email inválido")
        return jsonify(
            {"error" : "Formato de email inválido"}
        ), 403
    
    # Verificação se o email já existe no banco de dados
    try:
        assert not Usuario.query.filter_by(email = user_email).first()
    except:
        current_app.logger.error("Email já cadastrado")
        return jsonify(
            {"error" : "Email já cadastrado"}
        ), 401
    
    
    # Verificação da senha segura
    try:
        assert re.fullmatch(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', senha)
    except:
        return jsonify(
            {"error" : "Senha inválida, deve conter no mínimo 8 caracteres, dentre eles deva haver ao menos uma letra maúscula, uma minúscula e um número"}
        ), 403
        
    # Verificação se o nicname é único
    try:
        assert not Usuario.query.filter_by(nickname = nickname).first()
    except:
        return jsonify(
            {"error" : "Nickname já cadastrado"}
        ), 401
    
    while True:
        # Gerando um novo id
        new_id = secrets.token_hex(32)
        
        # Verificando se o nickname gerado já existe no banco de dados
        if not Usuario.query.filter_by(nickname = new_id).first():
            break
    
    # Caso todos os dados sejam válidos, cria um novo usuário
    return Usuario(
        id =  new_id,
        email = user_email,
        senha = senha,
        nickname = nickname,
        nome = nome,
        sobrenome = sobrenome
    )

