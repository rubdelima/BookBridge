from flask import Blueprint, jsonify, current_app
from src.database.models import db, Usuario, Clube, Participa
from src.database import model_validation as validator
from flask_caching import Cache

cache = Cache()

user_club_bp = Blueprint('/usuarios/clube', __name__)

@user_club_bp.route('/usuarios/clube/<clube_id>', methods=['POST'])
@validator.check_jwt_token
def post_user_clubs(current_user, clube_id):
    
    
    current_app.logger.info(f"Requisição para adicionar o user {current_user.id} ao grupo {clube_id} recebida")
    
    if not (clube := Clube.query.get(clube_id)):
        current_app.logger.error(f'Clube {clube_id} não encontrado')
        return jsonify({'error': 'Clube não encontrado'}), 404

    if (participa := Participa.query.get((current_user.id, clube_id))):
        current_app.logger.error(f'Já existe um registro de participação para o user {current_user.id} no clube {clube_id}')
        return jsonify({'error': 'Já existe um registro de participação'}), 409
    
    try:
        participa = Participa(
            usuario_id=current_user.id,
            clube_id=clube_id,
        )
        db.session.add(participa)
        db.session.commit()
        current_app.logger.info(f'Participação adicionada com sucesso para o user {current_user.id} no clube {clube_id}')
        return jsonify({'message': 'Participação adicionada com sucesso'}), 201

    except:
        db.session.rollback()
        current_app.logger.error('Erro ao salvar participação no banco de dados')
        return jsonify({'error': 'Erro ao salvar participação'}), 500


@user_club_bp.route('/usuarios/clube/<clube_id>', methods=['GET'])
@cache.cached(timeout=10)
def get_users_club(clube_id):
    
    current_app.logger.info(f"Requisição para listar os users do grupo {clube_id} recebida")
    
    if not (clube := Clube.query.get(clube_id)):
        current_app.logger.error(f'Clube {clube_id} não encontrado')
        return jsonify({'error': 'Clube não encontrado'}), 404
    
    try:
        users = db.session.query(Usuario).join(Participa).filter(Participa.clube_id == clube_id).all()
        
        if not users:
            current_app.logger.info(f'Nenhum usuário encontrado no clube {clube_id}')
            return jsonify({'message': 'Nenhum usuário encontrado'}), 200
    
        users_list = [{'id': user.id, 'nome': user.nome, 'sobrenome': user.sobrenome} for user in users]
        current_app.logger.info(f'Usuários encontrados no clube {clube_id}: {users_list}')

        return jsonify(users=users_list), 200

    except Exception as e:
        current_app.logger.exception(f'Erro ao buscar usuários do clube {clube_id}: {e}')
        return jsonify({'error': 'Erro interno no servidor'}), 500

@user_club_bp.route('/usuarios/clube/<clube_id>', methods=['DELETE'])
@validator.check_jwt_token
def delete_user_clubs(current_user, clube_id):
    
    current_app.logger.info(f"Requisição para remover o user {current_user.id} do grupo {clube_id} recebida")
    
    if not (clube := Clube.query.get(clube_id)):
        current_app.logger.error(f'Clube {clube_id} não encontrado')
        return jsonify({'error': 'Clube não encontrado'}), 404
    
    if not (participa := Participa.query.get((current_user.id, clube_id))):
        current_app.logger.error(f'Não existe um registro de participação para o user {current_user.id} no clube {clube_id}')
        return jsonify({'error': 'Não existe um registro de participação'}), 404
    
    try:
        db.session.delete(participa)
        db.session.commit()
        current_app.logger.info(f'Participação removida com sucesso para o user {current_user.id} no clube {clube_id}')
        return jsonify({'message': 'Participação removida com sucesso'}), 200
    except:
        db.session.rollback()
        current_app.logger.error('Erro ao tentar remover participação no banco de dados')
        return jsonify({'error': 'Erro ao tentar remover participação'}), 500

