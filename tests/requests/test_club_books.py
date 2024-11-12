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

def test_post_club_books(client, user_token):
    data = {
        "clube_id": "C003",
        "livro_id": "L016"
    }
    response = client.post(
        '/clube/livros',
        data=json.dumps(data),
        headers={'Authorization': f'Bearer {user_token}'},
        content_type='application/json'
    )

    assert response.status_code == 200
    assert 'message' in response.json
    assert response.json['message'] == 'Livro adicionado com sucesso ao grupo'

def test_get_club_books(client):
    clube_id = "C003"
    response = client.get(f'/clube/{clube_id}/livros')

    assert response.status_code == 200
    assert 'livros' in response.json
    assert isinstance(response.json['livros'], list)

def test_delete_club_books(client, user_token):
    data = {
        "clube_id": "C003",
        "livro_id": "L016"
    }
    response = client.delete(
        '/clube/livros',
        data=json.dumps(data),
        headers={'Authorization': f'Bearer {user_token}'},
        content_type='application/json'
    )

    assert response.status_code == 200
    assert 'message' in response.json
    assert response.json['message'] == 'Livro removido com sucesso do grupo'
