from flask import Blueprint, request, jsonify, current_app
from src.database.models import db, Usuario, Livro, Avaliacao, Clube, Participa, Adiciona
from src.database import model_validation as validator
from sqlalchemy.sql import func

club_books_bp = Blueprint('usuarios', __name__)

def validacao_books_club(data, user_id):
    """Validações para adicionar/editar um livro ao grupo de um usuário"""
    try:
        assert (book_id := data.get('livro_id')), ("livro_id",)
        assert (clube_id := data.get('clube_id')), ("clube_id",)
    
    except AssertionError as e:
        current_app.logger.error(f"O campo de {e.args[0]} não foi preenchido")
        return jsonify({'error': f"O campo de {e.args[0]} não foi preenchido"}), 400
    
    if not (Clube.query.get(clube_id)):
        current_app.logger.error(f'Clube {data["club_id"]} não encontrado')
        return jsonify({'error': 'Clube não encontrado'}), 404
    
    if not (Livro.query.get(book_id)):
        current_app.logger.error(f'Livro {data["livro_id"]} não encontrado')
        return jsonify({'error': 'Livro não encontrado'}), 404
    
    if not (Participa.query.get((user_id, clube_id))):
        current_app.logger.error(f'Não existe um registro de participação para o user {user_id} no clube {clube_id}')
        return jsonify({'error': 'Não é possível adicionar um livro em um clube que o usuário não participa'}), 403
    
    return (book_id, clube_id, 200)

@club_books_bp.route('/clube/livros', methods=['POST'])
@validator.check_jwt_token
def post_club_books(current_user):
    """
    ## Endpoint para adicionar um livro ao grupo de um usuário.

    Parâmetros de Entrada:
        - token : str (token de autenticação) - Deve ser enviado no header de Authorization
        - clube_id : str - Identificação do Clube
        - livro_id : str - Identificação do Livro
    """
    data = request.get_json()

    current_app.logger.info(f"Solicitaçao de Adição de Livro a um Grupo recebida, valores: {data}")
    
    validacao = validacao_books_club(data, current_user.id)
    
    if validacao[-1] != 200:
        return validacao
    
    book_id, clube_id, _ = validacao
    
    try:
        adiciona = Adiciona(usuario_id = current_user.id, livro_id=book_id, clube_id=clube_id)
        db.session.add(adiciona)
        db.session.commit()
        current_app.logger.info(f'Livro adicionado com sucesso ao grupo {clube_id} pelo user {current_user.id} do livro {book_id}')
        return jsonify({'message': 'Livro adicionado com sucesso ao grupo'}), 200
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Erro ao adicionar o livro ao grupo: {e}')
        return jsonify({'error': 'Erro ao adicionar o livro ao grupo'}), 500

@club_books_bp.route('/clube/<clube_id>/livros', methods=['GET'])
def list_club_books(clube_id):
    """
    ## Endpoint para listar os livros adicionados ao grupo de um usuário.

    Parâmetros de Entrada:
        - clube_id : str - Identificação do Clube
    """
    
    current_app.logger.info(f"Requisição para listar os livros do grupo {clube_id} recebida")
    
    clube = Clube.query.get(clube_id)
    if not clube:
        current_app.logger.error(f'Clube {clube_id} não encontrado')
        return jsonify({'error': 'Clube não encontrado'}), 404
    
    try:
        books_with_avg_rating = (
            db.session.query(
                Livro.id,
                Livro.nome,
                Livro.autor,
                func.coalesce(func.avg(Avaliacao.estrelas), None).label('media_avaliacoes')
            )
            .join(Adiciona, Adiciona.livro_id == Livro.id)
            .outerjoin(Avaliacao, Avaliacao.livro_id == Livro.id)
            .filter(Adiciona.clube_id == clube_id)
            .group_by(Livro.id, Livro.nome, Livro.autor)
        ).all()

        books_list = [
            {
                'id': book.id,
                'nome': book.nome,
                'autor': book.autor,
                'media_avaliacoes': book.media_avaliacoes
            }
            for book in books_with_avg_rating
        ]

        current_app.logger.info(f'Livros encontrados no clube {clube_id}: {books_list}')
        return jsonify(books=books_list), 200

    except Exception as e:
        current_app.logger.exception(f'Erro ao buscar livros do clube {clube_id}: {e}')
        return jsonify({'error': 'Erro interno no servidor'}), 500

@club_books_bp.route('/clube/livros', methods=['DELETE'])
@validator.check_jwt_token
def delete_club_books(current_user):
    
    data = request.get_json()

    current_app.logger.info(f"Solicitaçao de Adição de Livro a um Grupo recebida, valores: {data}")
    
    validacao = validacao_books_club(data, current_user.id)
    
    if validacao[-1] != 200:
        return validacao
    
    book_id, clube_id, _ = validacao
    
    try:
        adiciona = Adiciona.query.get((current_user.id, book_id, clube_id))
        db.session.delete(adiciona)
        db.session.commit()
        current_app.logger.info(f'Livro removido com sucesso do grupo {clube_id} pelo user {current_user.id} do livro {book_id}')
        return jsonify({'message': 'Livro removido com sucesso do grupo'}), 200
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Erro ao remover o livro do grupo: {e}')
        return jsonify({'error': 'Erro ao remover o livro do grupo'}), 500