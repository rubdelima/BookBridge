from src.database.models import db, Usuario, Clube, Livro, Participa, Adiciona
from datetime import datetime, timezone

# Teste para criar um clube
def test_create_clube(setup_database):
    clube = Clube(
        id='C001',
        criador='1234567890',
        nome='Clube Machado de Assis',
        description='Um clube para amantes de literatura clássica brasileira'
    )
    db.session.add(clube)
    db.session.commit()

    clube_criado = db.session.get(Clube, 'C001')
    assert clube_criado is not None
    assert clube_criado.nome == 'Clube Machado de Assis'

# Teste para ler um clube
def test_read_clube(setup_database):
    clube = db.session.get(Clube, 'C001')
    assert clube is not None
    assert clube.nome == 'Clube Machado de Assis'

# Teste para atualizar um clube
def test_update_clube(setup_database):
    clube = db.session.get(Clube, 'C001')
    clube.nome = 'Clube de Literatura Brasileira'
    db.session.commit()

    clube_atualizado = db.session.get(Clube, 'C001')
    assert clube_atualizado is not None
    assert clube_atualizado.nome == 'Clube de Literatura Brasileira'

# Teste para excluir um clube
def test_delete_clube(setup_database):
    clube = db.session.get(Clube, 'C001')
    db.session.delete(clube)
    db.session.commit()

    clube_excluido = db.session.get(Clube, 'C001')
    assert clube_excluido is None

# Teste para criar participação
def test_create_participa(setup_database):
    participa = Participa(
        usuario_id='1234567890',
        clube_id='C001'
    )
    db.session.add(participa)
    db.session.commit()

    participa_criado = db.session.get(Participa, ('1234567890', 'C001'))
    assert participa_criado is not None
    assert participa_criado.clube_id == 'C001'

# Teste para ler participação
def test_read_participa(setup_database):
    participa = db.session.get(Participa, ('1234567890', 'C001'))
    assert participa is not None
    assert participa.usuario_id == '1234567890'

# Teste para excluir participação
def test_delete_participa(setup_database):
    participa = db.session.get(Participa, ('1234567890', 'C001'))
    db.session.delete(participa)
    db.session.commit()

    participa_excluida = db.session.get(Participa, ('1234567890', 'C001'))
    assert participa_excluida is None

# Teste para criar uma entrada na tabela Adiciona
def test_create_adiciona(setup_database):
    livro = Livro(
        id='L124',
        autor='José de Alencar',
        nome='Iracema',
        genero='Romance',
        descricao='Uma das obras mais conhecidas de José de Alencar, retratando o mito da fundação do Ceará.'
    )
    db.session.add(livro)
    db.session.commit()

    adiciona = Adiciona(
        usuario_id='1234567890',
        clube_id='C001',
        livro_id='L124',
        data_adicao=datetime.now(tz=timezone.utc)
    )
    db.session.add(adiciona)
    db.session.commit()

    adiciona_criado = db.session.get(Adiciona, ('1234567890', 'C001', 'L124'))
    assert adiciona_criado is not None
    assert adiciona_criado.livro_id == 'L124'

# Teste para ler uma entrada na tabela Adiciona
def test_read_adiciona(setup_database):
    adiciona = db.session.get(Adiciona, ('1234567890', 'C001', 'L124'))
    assert adiciona is not None
    assert adiciona.livro_id == 'L124'

# Teste para excluir uma entrada na tabela Adiciona
def test_delete_adiciona(setup_database):
    adiciona = db.session.get(Adiciona, ('1234567890', 'C001', 'L124'))
    db.session.delete(adiciona)
    db.session.commit()

    adiciona_excluido = db.session.get(Adiciona, ('1234567890', 'C001', 'L124'))
    assert adiciona_excluido is None
