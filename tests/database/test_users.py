from src.database.models import db, Usuario
import uuid

# Teste para criar um usuário diretamente na database
def test_create_usuario(setup_database):
    usuario = Usuario(
        id='testUserId',
        email='testeUser@exemplo.com.br',
        senha='Senha@123',
        nickname='tester',
        nome='Maria',
        sobrenome='da Silva'
    )
    db.session.add(usuario)
    db.session.commit()

    usuario_criado = Usuario.query.filter_by(email='testeUser@exemplo.com.br').first()
    assert usuario_criado is not None
    assert usuario_criado.nickname == 'tester'

# Teste para ler o usuário na database
def test_read_usuario(setup_database):
    usuario = Usuario.query.filter_by(email='testeUser@exemplo.com.br').first()
    assert usuario is not None
    assert usuario.email == 'testeUser@exemplo.com.br'

# Teste para alterar as informações de um usuário na database
def test_update_usuario(setup_database):
    usuario = Usuario.query.filter_by(email='testeUser@exemplo.com.br').first()
    usuario.nome = 'Carlos'
    db.session.commit()

    usuario_atualizado = Usuario.query.filter_by(email='testeUser@exemplo.com.br').first()
    assert usuario_atualizado.nome == 'Carlos'

# Teste para excluir o usuário na database
def test_delete_usuario(setup_database):
    usuario = Usuario.query.filter_by(email='testeUser@exemplo.com.br').first()
    db.session.delete(usuario)
    db.session.commit()
    
    usuario_excluido = Usuario.query.filter_by(email='testeUser@exemplo.com.br').first()
    assert usuario_excluido is None