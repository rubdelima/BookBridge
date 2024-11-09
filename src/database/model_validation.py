from src.database.models import Usuario
from flask import jsonify
import re
import secrets
import string
import jwt
from functools import wraps
from flask import request, jsonify, current_app
from datetime import datetime, timedelta, timezone

current_app.config['SECRET_KEY'] = '936eb4f154867b74386f1bfc930ae0e7e8e4f9a759557dbfce0cb9f3a4a49edf'

def check_jwt_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token de autenticação é necessário'}), 403

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = Usuario.query.filter_by(id=data['user_id']).first()
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

def get_token(user_id):
    return jwt.encode({
        'user_id': user_id,
        'exp': datetime.now(tz=timezone.utc) + timedelta(days=7)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')

def valide_user(dados:dict)->Usuario:
    try:
        assert (user_email := dados.get('email'))
    except:
        return jsonify(
            {"error" : "O campo de email não foi preenchido"}
        ), 403
    
    # Verificação do pattern do email
    try:
        assert re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', user_email)
    except:
        return jsonify(
            {"error" : "Formato de email inválido"}
        ), 403
    
    # Verificação se o email já existe no banco de dados
    try:
        assert not Usuario.query.filter_by(email = user_email).first()
    except:
        return jsonify(
            {"error" : "Email já cadastrado"}
        ), 401
    
    # Verificação da senha
    
    # Verificação se o campo de senha foi preenchido
    try:
        assert (senha := dados.get('senha'))
    except:
        return jsonify(
            {"error" : "O campo de senha não foi preenchido"}
        ), 403
    
    # Verificação da senha segura
    try:
        assert re.fullmatch(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', senha)
    except:
        return jsonify(
            {"error" : "Senha inválida, deve conter no mínimo 8 caracteres, dentre eles deva haver ao menos uma letra maúscula, uma minúscula e um número"}
        ), 403
        
    # Verificação do Nickname do Usuário
    
    # Verificação se o campo de nickname foi preenchido
    try:
        assert (nickname := dados.get('nickname'))
    except:
        return jsonify(
            {"error" : "O campo de nickname não foi preenchido"}
        ), 403
    
    # Verificação se o nicname é único
    try:
        assert not Usuario.query.filter_by(nickname = nickname).first()
    except:
        return jsonify(
            {"error" : "Nickname já cadastrado"}
        ), 401
    
    # Verificação do Nome do Usuário
    
    # Verificação se o campo de nome foi preenchido
    try:
        assert (nome := dados.get('nome'))
    except:
        return jsonify(
            {"error" : "O campo de nome não foi preenchido"}
        ), 403
    
    # Verificação do Sobrenome do Usuário
    
    # Verificação se o campo de sobrenome foi preenchido
    try:
        assert (sobrenome := dados.get('sobrenome'))
    except:
        return jsonify(
            {"error" : "O campo de sobrenome não foi preenchido"}
        ), 403
    
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

