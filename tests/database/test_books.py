from src.database.models import db, Livro, Avaliacao, Usuario

# Teste para criar um livro
def test_create_livro(setup_database):
    livro = Livro(
        id='L123',
        autor='Machado de Assis',
        nome='Dom Casmurro',
        genero='Romance',
        descricao="Dom Casmurro, a obra mais conhecida do escritor Machado de Assis, conta a história de Bentinho e Capitu, que, apaixonados na adolescência, têm que enfrentar um obstáculo à realização de seus anseios amorosos, pois a mãe de Bentinho, D. Glória, fez uma promessa de que seu filho seria padre."
    )
    db.session.add(livro)
    db.session.commit()

    livro_criado = db.session.get(Livro, 'L123')
    assert livro_criado is not None
    assert livro_criado.nome == 'Dom Casmurro'

# Teste para ler um livro
def test_read_livro(setup_database):
    livro = db.session.get(Livro, 'L123')
    assert livro is not None
    assert livro.nome == 'Dom Casmurro'

# Teste para atualizar um livro
def test_update_livro(setup_database):
    livro = db.session.get(Livro, 'L123')
    livro.nome = 'Livro Atualizado'
    db.session.commit()

    livro_atualizado = db.session.get(Livro, 'L123')
    assert livro_atualizado is not None
    assert livro_atualizado.nome == 'Livro Atualizado'

# Teste para excluir um livro
def test_delete_livro(setup_database):
    livro = db.session.get(Livro, 'L123')
    db.session.delete(livro)
    db.session.commit()

    livro_excluido = db.session.get(Livro, 'L123')
    assert livro_excluido is None

# Teste para criar uma avaliação
def test_create_avaliacao(setup_database):
    avaliacao = Avaliacao(
        avaliador_id='1234567890',
        livro_id='L123',
        descricao='Ótimo livro!',
        estrelas=5,
    )
    db.session.add(avaliacao)
    db.session.commit()

    avaliacao_criada = db.session.get(Avaliacao, ('1234567890', 'L123'))
    assert avaliacao_criada is not None
    assert avaliacao_criada.estrelas == 5

# Teste para ler uma avaliação
def test_read_avaliacao(setup_database):
    avaliacao = db.session.get(Avaliacao, ('1234567890', 'L123'))
    assert avaliacao is not None
    assert avaliacao.descricao == 'Ótimo livro!'

# Teste para atualizar uma avaliação
def test_update_avaliacao(setup_database):
    avaliacao = db.session.get(Avaliacao, ('1234567890', 'L123'))
    avaliacao.estrelas = 4
    db.session.commit()

    avaliacao_atualizada = db.session.get(Avaliacao, ('1234567890', 'L123'))
    assert avaliacao_atualizada is not None
    assert avaliacao_atualizada.estrelas == 4

# Teste para excluir uma avaliação
def test_delete_avaliacao(setup_database):
    avaliacao = db.session.get(Avaliacao, ('1234567890', 'L123'))
    db.session.delete(avaliacao)
    db.session.commit()

    avaliacao_excluida = db.session.get(Avaliacao, ('1234567890', 'L123'))
    assert avaliacao_excluida is None

def test_verificar_avaliacoes(setup_database):
    usuario1 = Usuario(
        id='1234567890',
        email='user1@exemplo.com',
        senha='Senha@123',
        nickname='User1',
        nome='João',
        sobrenome='Silva'
    )
    usuario2 = Usuario(
        id='0987654321',
        email='user2@exemplo.com',
        senha='Senha@123',
        nickname='User2',
        nome='Maria',
        sobrenome='Oliveira'
    )
    db.session.add_all([usuario1, usuario2])
    db.session.commit()

    avaliacao1 = Avaliacao(
        avaliador_id='1234567890',
        livro_id='L123',
        descricao='Adorei o Romance, realmente o Machado de Assis é um dos maiores gênios literários da história',
        estrelas=5
    )
    avaliacao2 = Avaliacao(
        avaliador_id='0987654321',
        livro_id='L123',
        descricao='AFF, queria saber se Betina traiu ou não, sou curiosa, vou dar uma nota menor pq gostaria de saber mais 😒',
        estrelas=4
    )
    db.session.add_all([avaliacao1, avaliacao2])
    db.session.commit()

    resultado = db.session.\
        query(
            Usuario.nickname,
            Avaliacao.descricao,
            Avaliacao.estrelas,
            Avaliacao.data_avaliacao)\
        .join(Avaliacao, Usuario.id == Avaliacao.avaliador_id)\
        .filter(Avaliacao.livro_id == 'L123').all()

    assert len(resultado) == 2
    
    assert resultado[0].nickname == 'User1'
    assert resultado[0].descricao == 'Adorei o Romance, realmente o Machado de Assis é um dos maiores gênios literários da história'
    assert resultado[0].estrelas == 5

    assert resultado[1].nickname == 'User2'
    assert resultado[1].descricao == 'AFF, queria saber se Betina traiu ou não, sou curiosa, vou dar uma nota menor pq gostaria de saber mais 😒'
    assert resultado[1].estrelas == 4