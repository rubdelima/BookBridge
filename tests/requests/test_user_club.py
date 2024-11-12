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

def test_post_user_clubs(client, user_token):
    clube_id = "C002"
    response = client.post(
        f'/usuarios/clube/{clube_id}',
        headers={'Authorization': f'Bearer {user_token}'}
    )

    assert response.status_code == 201
    assert 'message' in response.json
    assert response.json['message'] == 'Participação adicionada com sucesso'

def test_get_users_club(client):
    clube_id = "C002"
    response = client.get(f'/usuarios/clube/{clube_id}')

    if response.status_code == 200:
        assert 'users' in response.json
        assert isinstance(response.json['users'], list)
    elif response.status_code == 404:
        assert 'error' in response.json
        assert response.json['error'] == 'Clube não encontrado'

def test_delete_user_clubs(client, user_token):
    clube_id = "C002"
    response = client.delete(
        f'/usuarios/clube/{clube_id}',
        headers={'Authorization': f'Bearer {user_token}'}
    )

    if response.status_code == 200:
        assert 'message' in response.json
        assert response.json['message'] == 'Participação removida com sucesso'
    elif response.status_code == 404:
        assert 'error' in response.json
        assert response.json['error'] == 'Clube não encontrado' or response.json['error'] == 'Não existe um registro de participação'
