from flask import Blueprint, request, jsonify, current_app
from src.database.models import db, Livro, Avaliacao
from src.database import model_validation as validator
import secrets
from sqlalchemy import or_

books_bp = Blueprint('livros', __name__)


@books_bp.route('/livros', methods=['POST'])
@validator.check_jwt_token
def post_livro(current_user):
    """
    Endpoint para criação de um novo livro.

    ---
    parameters:
      - name: Authorization
        in: header
        required: true
        description: Token de autenticação do usuário.
        schema:
          type: string
      - name: body
        in: body
        required: true
        description: Dados para criar um novo livro.
        schema:
          type: object
          properties:
            nome:
              type: string
              example: "Dom Casmurro"
            autor:
              type: string
              example: "Machado de Assis"
            genero:
              type: string
              example: "Romance"
            descricao:
              type: string
              example: "Um clássico da literatura brasileira."

    responses:
      201:
        description: Livro criado com sucesso.
      400:
        description: Campo de entrada não preenchido.
      401:
        description: Token de autenticação expirado.
      403:
        description: Token de autenticação inválido.
      500:
        description: Erro ao criar o livro.
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
def get_livro(livro_id):
    """
    Endpoint para busca de um livro específico pelo seu ID.

    ---
    parameters:
      - name: livro_id
        in: path
        required: true
        description: ID do livro.
        schema:
          type: string

    responses:
      200:
        description: Dados do livro retornados com sucesso.
      404:
        description: Livro não encontrado.
      500:
        description: Erro durante a busca do livro.
    """
    
    cache_key = f"livro_{livro_id}"
    
    cache = current_app.cache
    livro = cache.get(cache_key)
    
    if livro:
      current_app.logger.info(f"Cache hit para livro com id {livro_id}")
      return jsonify({"livro": livro}), 200
    
    current_app.logger.info(f"Requisição para busca do livro de id {livro_id}")
    
    if (livro := Livro.query.get(livro_id)):
        livro_dict = livro.to_dict()
        current_app.logger.info(f"Livro encontrado com sucesso: {livro_dict}")
        cache.set(cache_key, livro_dict, timeout=10)
        return jsonify({"livro" : livro_dict}), 200
    
    current_app.logger.error("Livro não encontrado")
    return jsonify({"error" : "Livro não encontrado"}), 404

@books_bp.route('/livros/buscar', methods=['GET'])
def get_livros():
    """
    Endpoint para busca de livros com base em parâmetros.

    ---
    parameters:
      - name: nome
        in: query
        required: false
        description: Título do livro.
        schema:
          type: string
      - name: autor
        in: query
        required: false
        description: Autor do livro.
        schema:
          type: string
      - name: genero
        in: query
        required: false
        description: Gênero do livro.
        schema:
          type: string

    responses:
      200:
        description: Livros retornados com sucesso.
        content:
          application/json:
            schema:
              type: object
              properties:
                livros:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: string
                      nome:
                        type: string
                      autor:
                        type: string
                      genero:
                        type: string
      400:
        description: Parâmetros de busca inválidos.
      500:
        description: Erro durante a busca dos livros.
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
    Endpoint para criação de uma nova avaliação.

    ---
    parameters:
      - name: Authorization
        in: header
        required: true
        description: Token de autenticação do usuário.
        schema:
          type: string
      - name: body
        in: body
        required: true
        description: Dados para criar uma avaliação.
        schema:
          type: object
          properties:
            livro_id:
              type: string
              example: "12345"
            descricao:
              type: string
              example: "Excelente livro!"
            estrelas:
              type: integer
              example: 5

    responses:
      201:
        description: Avaliação criada com sucesso.
      400:
        description: Campo de entrada não preenchido ou incorreto.
      401:
        description: Token de autenticação expirado.
      403:
        description: Token de autenticação inválido.
      404:
        description: Livro não encontrado.
      500:
        description: Erro ao criar a avaliação.
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