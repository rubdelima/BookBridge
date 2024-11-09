from src.database.models import Usuario
from flask import jsonify
import re
import random
import string

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
        new_id = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=10))
        
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

