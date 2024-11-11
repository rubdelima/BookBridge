from flask import Blueprint, request, jsonify, current_app
from src.database.models import db, Usuario
from src.database import model_validation as validator
from sqlalchemy import or_
import re

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
    Endpoint para listar os dados do usuário logado.

    Parâmetros de Entrada:
        - token : str (token de autenticação) Deve ser enviado no header de Authorization

    Retorno:
        - 200 : OK - Se os dados do usuário foram retornados com sucesso
        - 401 : Not authorized - Se o token de autenticação está espirado
        - 403 : Forbidden - Se o token de autenticação não é válido
        - 500 : Internal Server Error - Se houve algum erro durante a listagem dos dados
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
    ## Endpoint para a exclusão de um usuario

    Parâmetros de Entrada:
        - token : str (token de autenticação) Deve ser enviado no header de Authorization

    Retorno:
    - 200 : OK - Se o usuário foi excluído com sucesso
    - 401 : Not authorized - Se o token de autenticação está espirado
    - 403 : Forbidden - Se o token de autenticação não é válido
    - 500 : Internal Server Error - Se houve algum erro durante a exclusão do usuário
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
