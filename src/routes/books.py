from flask import Blueprint, request, jsonify, current_app
from src.database.models import db, Livro, Avaliacao
from src.database import model_validation as validator
import secrets
from sqlalchemy import or_
from flask_caching import Cache

cache = Cache()

books_bp = Blueprint('livros', __name__)


@books_bp.route('/livros', methods=['POST'])
@validator.check_jwt_token
def post_livro(current_user):
    """
    ## Endpoint para criação de um novo livro.

    Parâmetros de Entrada:
        - token : str (token de autenticação) - Deve ser enviado no header de Authorization
        - nome : str - Título do livro
        - autor : str - Autor do livro
        - genero : str - Genero do livro
        - descricao : str - Descrição do livro

    Retorno:
        - 201 : OK - Se os dados do livro foram criados com sucesso
        - 401 : Not authorized - Se o token de autenticação está espirado
        - 403 : Forbidden - Se o token de autenticação não é válido
        - 500 : Internal Server Error - Se houve algum erro durante a criação do livro
    """

    data = request.json

    current_app.logger.info(f"Requisição de POST de livro recebida: {data}")
    
    try:
        assert (nome := data.get('nome')), ("nome",)
        assert (autor := data.get('autor')),  ('autor',)
        assert (genero := data.get('genero')), ('genero',)
        assert (descricao := data.get('descricao')), ("descricao", )
    
    except AssertionError as e:
        current_app.logger.error(f"O campo de {e.args[0]} não foi preenchido")
        return jsonify({'error': f"O campo de {e.args[0]} não foi preenchido"}), 400

    try:
        livro = Livro(id=secrets.token_hex(), autor=autor,
                      nome=nome, genero=genero, descricao=descricao)
        db.session.add(livro)
        db.session.commit()
        current_app.logger.info("Livro criado com sucesso")
        return jsonify({'message': 'Livro criado com sucesso'}), 201

    except Exception as e:
        db.session.rollback()
        current_app.logger.exception(e)
        return jsonify({"error": str(e)}), 500

@books_bp.route('/livros/<livro_id>', methods=['GET'])
@cache.cached(timeout=10, query_string=True)
def get_livro(livro_id):
    """
    ## Endpoint para busca de um livro específico pelo seu id
    
    ### Parâmetros de Entrada:

    - livro_id : str (ID do livro)

    ### Códigos de Retorno:

    - 200 : OK - Se os dados do livro foram retornados com sucesso

    - 404 : Not Found - Se o livro não foi encontrado

    - 500 : Internal Server Error - Se houve algum erro durante a busca do livro

    ### Retorno

    - livro : Livro

    """
    current_app.logger.info(f"Requisição para busca do livro de id {livro_id}")
    
    if (livro := Livro.query.get(livro_id)):
        livro_dict = livro.to_dict()
        current_app.logger.info(f"Livro encontrado com sucesso: {livro_dict}")
        return jsonify({"livro" : livro_dict}), 200
    
    current_app.logger.error("Livro não encontrado")
    return jsonify({"error" : "Livro não encontrado"}), 404

@books_bp.route('/livros/buscar', methods=['GET'])
@cache.cached(timeout=10)
def get_livros():
    """
    ## Endpoint para busca de um livro a seguir pelos parâmetros indicados

    ### Parâmetros de Entrada:


    - nome : str (Título do livro)

    - autor : str (Autor do livro)

    - genero : str (Genero do livro)

    ### Códigos de Retorno:

    - 200 : OK - Se os dados do livro foram retornados com sucesso

    - 400 : Bad Request - Se os parâmetros de busca estão incorretos

    - 500 : Internal Server Error - Se houve algum erro durante a listagem dos dados

    ### Retorno

    - livros : list[Livros]

    """

    current_app.logger.info(f"Requisição de POST de busca de livros recebida: {request.args}")
    
    nome = request.args.get('nome')
    autor = request.args.get('autor')
    genero = request.args.get('genero')

    if not (nome or autor or genero):
        current_app.logger.error("Parâmetros de busca inválidos")
        return jsonify({'error': 'Parâmetros de busca inválidos'}), 400

    try:
        query = Livro.query
        filters = []

        if nome:
            filters.append(Livro.nome.contains(nome))
        if autor:
            filters.append(Livro.autor.contains(autor))
        if genero:
            filters.append(Livro.genero.contains(genero))

        if filters:
            query = query.filter(or_(*filters))

        livros = query.all()
        
        if len(livros) == 0:
            current_app.logger.info("Nenhum livro encontrado com os dados fornecidos")
            return jsonify(livros=[]), 200
        current_app.logger.info(f"Livros encontrados com sucesso")
        return jsonify(livros=[livro.to_dict() for livro in livros]), 200
    
    except Exception as e:
        current_app.logger.exception(f"Erro durante a busca de livros: {e}")
        return jsonify({'error': 'Erro interno no servidor'}), 500

@books_bp.route('/livros/avaliar', methods=['POST'])
@validator.check_jwt_token
def post_avaliacao(current_user):
    """
    ## Endpoint para criação de uma nova avaliação.

    Parâmetros de Entrada:
        - token : str (token de autenticação) - Deve ser enviado no header de Authorization
        - livro_id : str - Identificação do Livro
        - descricao : str - Descrição da avaliação
        - estrelas : int - Número de estrelas da avaliação (1-5)

    Retorno:
        - 200 : OK - Se os dados do usuário foram retornados com sucesso
        - 401 : Not authorized - Se o token de autenticação está espirado
        - 403 : Forbidden - Se o token de autenticação não é válido
        - 500 : Internal Server Error - Se houve algum erro durante a listagem dos dados
    """

    data = request.json
    current_app.logger.info(f"Requisição de Post de Avaliação, {data}")
    
    try:
        assert (livro_id := data.get('livro_id')), ("livro_id",)
        assert (descricao := data.get('descricao')), ("descricao",)
        assert (estrelas := int(data.get('estrelas'))), ("estrelas",)
        assert 0 <= estrelas <= 5, ("estrelas",)
    except AssertionError as e:
        current_app.logger.error(f"O campo de {e.args[0]} não foi preenchido ou foi preenchido incorretamente")
        return jsonify({'error': f"O campo de {e.args[0]} não foi preenchido ou foi preenchido incorretamente"}), 400

    try:
        assert (Livro.query.get(livro_id))
    except:
        current_app.logger.error("Livro não encontrado")
        return jsonify({"error": "Livro não encontrado"}), 404

    try:
        avaliacao = Avaliacao(
            avaliador_id=current_user.id,
            livro_id=livro_id,
            descricao=descricao,
            estrelas=estrelas,
        )

        db.session.add(avaliacao)
        db.session.commit()
        current_app.logger.info('Avaliação realizada com sucesso')
        return jsonify({'message': 'Avaliação realizada com sucesso'}), 201

    except Exception as e:
        db.session.rollback()
        current_app.logger.exception(str(e))
        return jsonify({"error": str(e)}), 500