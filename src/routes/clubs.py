from flask import Blueprint, request, jsonify, current_app
from src.database.models import db, Clube, Participa
from src.database import model_validation as validator
import secrets
from datetime import datetime, timezone

clubs_bp = Blueprint('clubes', __name__)

@clubs_bp.route('/clubes', methods=['POST'])
@validator.check_jwt_token
def post_club(current_user):
    """
    Endpoint para criação de um novo clube de livros.

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
        description: Dados do novo clube de livros.
        schema:
          type: object
          properties:
            nome:
              type: string
              example: "Clube de Ficção Científica"
            descricao:
              type: string
              example: "Clube para discutir livros de ficção científica."

    responses:
      201:
        description: Clube de livros criado com sucesso.
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Clube de Livros Criado com Sucesso!"
      400:
        description: Erro de validação.
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "O campo de nome não foi preenchido"
      403:
        description: Usuário não autenticado.
      500:
        description: Erro ao tentar salvar o clube.
    """
    
    data = request.json
    current_app.logger.info(f"Requisição de POST de clube recebida: {data}")
    
    try:
        assert (nome := data.get('nome')), ("nome",)
        assert (description := data.get('descricao')), ("descricao",)
    except AssertionError as e:
        current_app.logger.error(f"O campo de {e.args[0]} não foi preenchido")
        return jsonify({'error': f"O campo de {e.args[0]} não foi preenchido"}), 400
    
    try:
        while True:
            club_id = secrets.token_hex()
            if not Clube.query.get(club_id):
                break
            
        club = Clube(
            id=club_id,
            nome=nome,
            descricao=description,
            criador=current_user.id
        )
        db.session.add(club)
        db.session.commit()
        
        db.session.add(
            Participa(
                usuario_id=current_user.id,
                clube_id=club_id,
            )
        )
        db.session.commit()
        
        return jsonify({"message": "Clube de Livros Criado com Sucesso!",}), 200
    except Exception as e:
        current_app.logger.error(f"Erro ao tentar salvar o clube: {e}")
        return jsonify({'error': 'Erro ao tentar salvar o clube'}), 500
    
@clubs_bp.route('/clubes/<club_id>', methods=['GET'])
def get_club(club_id):
    """
    Endpoint para busca de um clube específico pelo seu ID.

    ---
    parameters:
      - name: club_id
        in: path
        required: true
        description: ID do clube a ser buscado.
        schema:
          type: string

    responses:
      200:
        description: Dados do clube retornados com sucesso.
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: string
                nome:
                  type: string
                description:
                  type: string
      404:
        description: Clube não encontrado.
      500:
        description: Erro interno ao buscar clube.
    """
    cache_key = f"/clubes/{club_id}"
    cache = current_app.cache
    clube = cache.get(cache_key)
    
    if clube:
      current_app.logger.info(f"Clube encontrado no cache: {clube}")
      return jsonify(clube), 200
    
    try:
        assert (club := request.json.get('club_id'))
        
    except AssertionError:
        current_app.logger.error(f"O campo de club_id não foi preenchido")
        return jsonify({'error': 'O campo de club_id não foi preenchido'}), 400
    
    club = Clube.query.get(club)
    
    if not club:
        current_app.logger.error("Clube não encontrado")
        return jsonify({'error': 'Clube não encontrado'}), 404
    club_dict = club.to_dict()
    current_app.logger.info(f"Clube encontrado com sucesso: {club_dict}")
    cache.set(cache_key, club_dict, timeout=10)
    return jsonify(club_dict), 200
    
@clubs_bp.route('/clubes/buscar', methods=['GET'])
def find_clubs():
    """
    Endpoint para busca de clubes por nome.

    ---
    parameters:
      - name: nome
        in: query
        required: true
        description: Nome do clube a ser buscado.
        schema:
          type: string

    responses:
      200:
        description: Clubes encontrados com sucesso.
        content:
          application/json:
            schema:
              type: object
              properties:
                clubes:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: string
                      nome:
                        type: string
                      description:
                        type: string
      404:
        description: Nenhum clube encontrado.
      400:
        description: Campo de nome não preenchido.
      500:
        description: Erro ao buscar clubes.
    """
    
    nome = request.args.get('nome')
    
    if not nome:
        current_app.logger.error("O campo de nome não foi preenchido")
        return jsonify({'error': 'O campo de nome não foi preenchido'}), 400
    current_app.logger.info(f"Buscando clubes com nome: {nome}")

    try:
        clubs = list(map(lambda x : x.to_dict(), Clube.query.filter(Clube.nome.contains(nome)).all()))
        
        if not clubs:
            current_app.logger.info("Nenhum clube encontrado")
            return jsonify({'error': 'Nenhum clube encontrado'}), 404
        
        current_app.logger.info(f"Clubes encontados: {clubs}")
        return jsonify({'clubes' : clubs}), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro ao buscar clubes: {e}")
        return jsonify({'error': 'Erro ao buscar clubes'}), 500

@clubs_bp.route('/clubes/<club_id>', methods=['PUT'])
@validator.check_jwt_token
def update_club(current_user, club_id):
    """
    Endpoint para atualizar as informações de um clube.

    ---
    parameters:
      - name: Authorization
        in: header
        required: true
        description: Token de autenticação do usuário.
        schema:
          type: string
      - name: club_id
        in: path
        required: true
        description: ID do clube a ser atualizado.
        schema:
          type: string
      - name: body
        in: body
        required: true
        description: Dados a serem atualizados no clube.
        schema:
          type: object
          properties:
            nome:
              type: string
              example: "Novo Nome do Clube"
            descricao:
              type: string
              example: "Descrição atualizada do clube."

    responses:
      200:
        description: Clube atualizado com sucesso.
      403:
        description: Usuário não é criador do clube.
      404:
        description: Clube não encontrado.
      500:
        description: Erro ao tentar atualizar o clube.
    """
    
    current_app.logger.info(
        f'Requisição de PUT do clube {club_id} feito pelo user {current_user.id}'
    )
    
    
    if not (club := Clube.query.get(club_id)):
        current_app.logger.error(f'Clube {club_id} não encontrado')
        return jsonify({'error': 'Clube não encontrado'}), 404

    data = request.json
    
    if club.criador != current_user.id:
        current_app.logger.error('Usuário não é criador do clube')
        return jsonify({'error': 'Usuário não é criador do clube'}), 403
    
    for field in {'nome', 'description'} & set(data.keys()):
        setattr(club, field, data[field])
    
    try:
        db.session.commit()
        current_app.logger.info(f'Clube {club_id} atualizado com sucesso')
        return jsonify({'message': 'Clube atualizado com sucesso'}), 200
    except Exception as e:
        current_app.logger.error(f'Erro ao tentar atualizar o clube {club_id}: {e}')
        return jsonify({'error': 'Erro ao tentar atualizar o clube'}), 500

@clubs_bp.route('/clubes/<club_id>', methods=['DELETE'])
@validator.check_jwt_token
def delete_club(current_user, club_id):
    """
    Endpoint para deletar um clube.

    ---
    parameters:
      - name: Authorization
        in: header
        required: true
        description: Token de autenticação do usuário.
        schema:
          type: string
      - name: club_id
        in: path
        required: true
        description: ID do clube a ser deletado.
        schema:
          type: string

    responses:
      200:
        description: Clube deletado com sucesso.
      403:
        description: Usuário não é criador do clube.
      404:
        description: Clube não encontrado.
      500:
        description: Erro ao tentar deletar o clube.
    """
    
    current_app.logger.info(
        f'Requisição de DELETE do clube {club_id} feito pelo user {current_user.id}'
    )
    
    if not (club := Clube.query.get(club_id)):
        current_app.logger.error(f'Clube {club_id} não encontrado')
        return jsonify({'error': 'Clube não encontrado'}), 404
    
    if club.criador != current_user.id:
        current_app.logger.error('Usuário não é criador do clube')
        return jsonify({'error': 'Usuário não é criador do clube'}), 403
    
    try:
        db.session.delete(club)
        db.session.commit()
        current_app.logger.info(f'Clube {club_id} deletado com sucesso')
        return jsonify({'message': 'Clube deletado com sucesso'}), 200
    
    except Exception as e:
        current_app.logger.error(f'Erro ao tentar deletar o clube {club_id}: {e}')
        return jsonify({'error': 'Erro ao tentar deletar o clube'}), 500
