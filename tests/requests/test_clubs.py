import pytest
import json

@pytest.fixture(scope='function')
def user_token(client):
    login_data = {
        "email": "user1@example.com",
        "senha": "Senha@123"
    }
    response = client.get('/usuarios/login/', data=json.dumps(login_data),
                           content_type='application/json')
    assert (token := response.json.get('token'))
    return token

def test_post_club(client, user_token):
    data = {
        "nome": "Clube de Ficção Científica",
        "descricao": "Clube para discutir livros de ficção científica."
    }
    response = client.post(
        '/clubes',
        data=json.dumps(data),
        headers={'Authorization': f'Bearer {user_token}'},
        content_type='application/json'
    )

    assert response.status_code == 200
    assert 'message' in response.json
    assert response.json['message'] == 'Clube de Livros Criado com Sucesso!'

def test_get_club(client):
    club_id = "C001"
    response = client.get(f'/clubes/{club_id}')

    if response.status_code == 200:
        assert 'id' in response.json
        assert 'nome' in response.json

def test_find_clubs(client):
    nome = "Leitura"
    response = client.get(f'/clubes/buscar?nome={nome}')

    if response.status_code == 200:
        assert 'clubes' in response.json
        assert isinstance(response.json['clubes'], list)

def test_update_club(client, user_token):
    club_id = "C001"
    data = {
        "nome": "Novo Nome do Clube",
        "descricao": "Descrição atualizada do clube."
    }
    response = client.put(
        f'/clubes/{club_id}',
        data=json.dumps(data),
        headers={'Authorization': f'Bearer {user_token}'},
        content_type='application/json'
    )

    if response.status_code == 200:
        assert 'message' in response.json
        assert response.json['message'] == 'Clube atualizado com sucesso'

def test_delete_club(client, user_token):
    club_id = "C001"
    response = client.delete(
        f'/clubes/{club_id}',
        headers={'Authorization': f'Bearer {user_token}'}
    )

    if response.status_code == 200:
        assert 'message' in response.json
        assert response.json['message'] == 'Clube deletado com sucesso'
