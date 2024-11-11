from flask import Blueprint, request, jsonify, current_app
from src.database.models import db, Clube, Participa
from src.database import model_validation as validator
import secrets
from datetime import datetime, timezone
from flask_caching import Cache

cache = Cache(current_app)

clubs_bp = Blueprint('clubes', __name__)

@clubs_bp.route('/clubes', methods=['POST'])
@validator.check_jwt_token
def post_club(current_user):
    """
    ## Endpoint para criação de um novo livro.

    Parâmetros de Entrada:
        - token : str (token de autenticação) - Deve ser enviado no header de Authorization
        - nome: str (Nome do Clube de Livros)
        - description : str (Descrição do Clube de Livros)
    Retorno:
        - 201 : OK - Se os dados do Clube de Livros foram criados com sucesso
        - 403 : Usuário nâo autenticado
        - 400 : Erro de validação
    """
    
    data = request.json
    current_app.logger.info(f"Requisição de POST de clube recebida: {data}")
    
    try:
        assert (nome := data.get('nome')), ("nome",)
        assert (description := data.get('description')), ("description",)
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
            description=description,
            usuario_criador_id=current_user.id
        )
        db.session.add(club)
        db.session.commit()
        
        db.session.add(
            Participa(
                usuario_id=current_user.id,
                clube_id=club_id,
                data_participacao=datetime.now(tz=timezone.utc)
            )
        )
        db.session.commit()
        
        return jsonify({"message": "Clube de Livros Criado com Sucesso!",}), 200
    except Exception as e:
        current_app.logger.error(f"Erro ao tentar salvar o clube: {e}")
        return jsonify({'error': 'Erro ao tentar salvar o clube'}), 500
    
@clubs_bp.route('/clubes/<club_id>', methods=['GET'])
@cache.cached(timeout=10)
def get_club(club_id):
    """
    ## Endpoint para busca de um clube específico pelo seu id
    
    ### Parâmetros de Entrada:

    - club_id : str (ID do Clube)

    ### Códigos de Retorno:
        - 200 : OK - Se os dados do Clube de Livros foram encontrados
        - 404 : Clube não encontrado
    """
    
    try:
        assert (club := request.json.get('club_id'))
        
    except AssertionError:
        current_app.logger.error(f"O campo de club_id não foi preenchido")
        return jsonify({'error': 'O campo de club_id não foi preenchido'}), 400
    
    club = Clube.query.get(club)
    
    if not club:
        current_app.logger.error("Clube não encontrado")
        return jsonify({'error': 'Clube não encontrado'}), 404
    
    current_app.logger.info(f"Clube encontrado com sucesso: {club.to_dict()}")
    return jsonify(club.to_dict()), 200
    
@clubs_bp.route('/clubes/buscar', methods=['GET'])
def find_clubs():
    """
    ## Endpoint para busca de clubes por nome

    ### Parâmetros de Entrada:
        - nome : str (Nome do Clube)

    ### Códigos de Retorno:
        - 200 : OK - Se os dados do Clube de Livros foram encontrados
        - 404 : Nenhum clube encontrado
        - 500 : Erro interno
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
    
    """
    
    current_app.logger.info(
        f'Requisição de PUT do clube {club_id} feito pelo user {current_user.id}'
    )
    
    
    if not (club := Clube.query.get(current_user)):
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
    
    """
    
    current_app.logger.info(
        f'Requisição de DELETE do clube {club_id} feito pelo user {current_user.id}'
    )
    
    if not (club := Clube.query.get(current_user)):
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
