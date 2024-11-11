from flask import Blueprint, request, jsonify, current_app
from src.database.models import db, Usuario
from src.database import model_validation as validator
from sqlalchemy import or_
import re

users_bp = Blueprint('usuarios', __name__)


@users_bp.route('/usuarios', methods=['POST'])
def post_user():
    """
    Criação de um novo usuário
    ---
    tags:
      - Usuário
    parameters:
      - in: body
        name: body
        required: true
        description: Dados do novo usuário
        schema:
          type: object
          properties:
            email:
              type: string
              example: "exemplo@dominio.com"
            senha:
              type: string
              example: "Senha@123"
            nickname:
              type: string
              example: "apelido123"
            nome:
              type: string
              example: "João"
            sobrenome:
              type: string
              example: "Silva"
    responses:
      201:
        description: Usuário criado com sucesso
      401:
        description: E-mail ou nickname já cadastrado
      403:
        description: Campo(s) não preenchido(s) corretamente
      500:
        description: Erro interno no servidor
    """

    current_app.logger.info(
        f"Requisição de POST de usuário recebida, conteudo: {request.json}")

    # Validação dos campos do Usuário
    user = validator.valide_user(request.json)
    if not isinstance(user, Usuario):
        return user

    try:
        # Salva o novo usuário no banco de dados
        db.session.add(user)
        db.session.commit()
        token = validator.get_token(user.id)
        current_app.logger.info(f"Usuário criado com sucesso, token: {token}")
        return jsonify({'token': token}), 200

    except Exception as e:
        # Desfaz alteracões e retorna o erro
        db.session.rollback()
        current_app.logger.exception(str(e))
        return jsonify({"error": str(e)}), 500


@users_bp.route('/usuarios/login/', methods=['GET'])
def login_user():
    """
    Login de um usuário
    ---
    tags:
      - Usuário
    parameters:
      - in: body
        name: body
        required: true
        description: Dados para login do usuário
        schema:
          type: object
          properties:
            email:
              type: string
              example: "usuario@example.com"
            nickname:
              type: string
              example: "user123"
            senha:
              type: string
              example: "Senha@123"
    responses:
      200:
        description: Login realizado com sucesso
        schema:
          type: object
          properties:
            token:
              type: string
      401:
        description: Email, nickname ou senha incorretos
      500:
        description: Erro interno no servidor
    """

    current_app.logger.info(
        f"Requisição de LOGIN/GET de usuário recebida, dados recebidos: {request.json}")

    dados = request.json
    nickname, email = None, None
    try:
        assert (senha := dados.get('senha')), ('senha', )
        assert (email := dados.get('email')) or (
            nickname := dados.get('nickname')), ('email ou nickname')

    except AssertionError as ae:
        current_app.logger.error(f"O campo de {ae.args[0]} não foi preenchido")

        return jsonify(
            {"error": f"O campo de {ae.args[0]} não foi preenchido"}
        ), 403

    try:
        user = Usuario.query.filter(
            or_(Usuario.email == email, Usuario.nickname == nickname)
        ).first()

        assert user and (user.senha == senha)

    except AssertionError:
        current_app.logger.error("Email, nickname ou senha incorretos")
        return jsonify(

            {"error": "Email, nickname ou senha incorretos"}
        ), 401

    except Exception as e:
        current_app.logger.exception(f'Erro durante o login {e}')
        return jsonify({"error": "Ocorreu um erro durante o login"}), 500

    try:
        db.session.add(user)
        db.session.commit()
        token = validator.get_token(user.id)
        current_app.logger.info("Usuário logado com sucesso!")
        return jsonify({'token': token}), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.exception(f'Erro durante o login {e}')
        return jsonify({"error": "Ocorreu um erro durante o login"}), 500


@users_bp.route('/usuarios', methods=['GET'])
@validator.check_jwt_token
def get_user(current_user):
    """
    Retorna os dados do usuário logado
    ---
    tags:
      - Usuário
    parameters:
      - in: header
        name: Authorization
        required: true
        description: Token de autenticação (formato: Bearer token)
        type: string
    responses:
      200:
        description: Dados do usuário retornados com sucesso
        schema:
          type: object
      401:
        description: Token expirado
      403:
        description: Token de autenticação inválido
      500:
        description: Erro durante a listagem dos dados do usuário
    """

    current_app.logger.info(
        f"Requisição de GET do usuário {current_user.id} recebida"
    )

    try:
        user_dict = current_user.to_dict()
        current_app.logger.info(
            f"Usuário {current_user.id} retornado com sucesso")
        return jsonify(user_dict), 200

    except Exception as e:
        current_app.logger.exception(e)
        return jsonify({"error": "Ocorreu um erro durante a listagem dos dados"}), 500


@users_bp.route('/usuarios', methods=['PUT'])
@validator.check_jwt_token
def update_user(current_user):
    """
    Atualiza os dados do usuário logado
    ---
    tags:
      - Usuário
    parameters:
      - in: header
        name: Authorization
        required: true
        description: Token de autenticação (formato: Bearer token)
        type: string
      - in: body
        name: body
        required: true
        description: Dados do usuário para atualização
        schema:
          type: object
          properties:
            email:
              type: string
              example: "novoemail@example.com"
            senha:
              type: string
              example: "NovaSenha@123"
            nickname:
              type: string
              example: "novonick123"
            nome:
              type: string
              example: "NovoNome"
            sobrenome:
              type: string
              example: "NovoSobrenome"
    responses:
      200:
        description: Usuário atualizado com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
            atualizados:
              type: array
              items:
                type: string
            erros:
              type: array
              items:
                type: string
      400:
        description: Não foi possível atualizar os campos
      401:
        description: Token expirado
      403:
        description: Token de autenticação inválido
      500:
        description: Erro durante a atualização dos dados
    """

    current_app.logger.info(
        f"Requisição de PUT do usário {current_user.id} recebida com os parametros : {request.json}"
    )

    dados = request.json

    to_update = {'email', 'senha', 'nickname',
                 'nome', 'sobrenome'} & set(dados.keys())

    updated = []
    errors = []

    for field in to_update:
        try:
            if field == 'email':
                assert re.fullmatch(
                    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', dados.get(field))
                user = Usuario.query.filter_by(email=dados.get(field)).first()
                assert user is None or user.id == current_user.id

            elif field == 'senha':
                assert re.fullmatch(
                    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', dados.get(field))

            elif field == 'nickname':
                user = Usuario.query.filter_by(
                    nickname=dados.get(field)).first()
                assert user is None or user.id == current_user.id

            setattr(current_user, field, dados.get(field))

            db.session.commit()
            updated.append(field)
        except:
            db.session.rollback()
            current_app.logger.error(f"Erro ao tentar atualizar o campo {field}, {dados.get(field)}")
            errors.append(field)

    if len(updated) == 0 and errors > 1:
        current_app.logger.error(
            f"Não foi possível atualizar todos os campos: {', '.join(errors)}")
        return jsonify(
            {"error": f"Não foi possível atualizar todos os campos: {', '.join(errors)}"}
        ), 400
    
    current_app.logger.info(f"Usuário atualizado com sucesso, atualizados: {updated}, erros: {errors}")
    
    return jsonify(
        {"message": "Usuário atualizado com sucesso",
            "atualizados": updated, "erros": errors}
    ), 200


@users_bp.route('/usuarios', methods=['DELETE'])
@validator.check_jwt_token
def delete_user(current_user):
    """
    Exclusão de um usuário
    ---
    tags:
      - Usuário
    parameters:
      - in: header
        name: Authorization
        required: true
        description: Token de autenticação (formato: Bearer token)
        type: string
    responses:
      200:
        description: Usuário excluído com sucesso
      401:
        description: Token expirado
      403:
        description: Token de autenticação inválido
      500:
        description: Erro durante a exclusão do usuário
    """
    current_app.logger.info(f"Requisição DELETE do usuário {current_user.id}")
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
    Busca um usuário pelo nickname
    ---
    tags:
      - Usuário
    parameters:
      - in: header
        name: Authorization
        required: true
        description: Token de autenticação (formato: Bearer token)
        type: string
      - in: path
        name: nickname
        required: true
        description: Nickname do usuário
        type: string
    responses:
      200:
        description: Usuário encontrado com sucesso
        schema:
          type: object
      401:
        description: Token expirado
      403:
        description: Token de autenticação inválido
      404:
        description: Usuário não encontrado
      500:
        description: Erro durante a busca do usuário
    """

    current_app.logger.info(f"Buscando o nickname: {nickname}")
    
    user = Usuario.query.filter_by(nickname=nickname).first()

    if not user:
        current_app.logger.error(f"Usuário {nickname} não encontrado")
        return jsonify({"error": "Usuário não encontrado"}), 404

    current_app.logger.info(f"Usuário {nickname} encontrado com sucesso")
    return jsonify(user.to_dict()), 200
