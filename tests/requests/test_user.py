import pytest
import json


@pytest.fixture(scope='module')
def new_user_data():
    return {
        "email": "test@example.com",
        "senha": "Senha@123",
        "nickname": "testuser",
        "nome": "Test",
        "sobrenome": "User"
    }


@pytest.fixture(scope='function')
def user_token(client):
    login_data = {
        "email": "test@example.com",
        "senha": "Senha@123"
    }
    response = client.get('/usuarios/login/', data=json.dumps(login_data),
                           content_type='application/json')
    assert (token := response.json.get('token'))
    return token


def test_create_user(client, new_user_data):
    """Teste para criação de um novo usuário"""
    response = client.post(
        '/usuarios', data=json.dumps(new_user_data), content_type='application/json')
    assert response.status_code == 200
    assert 'token' in response.json


def test_login_user(client):
    """Teste para login de um usuário existente com token"""
    login_data = {
        "email": "test@example.com",
        "senha": "Senha@123"
    }
    response = client.get('/usuarios/login/', data=json.dumps(login_data),
                           content_type='application/json')
    assert response.status_code == 200
    assert 'token' in response.json

def test_login_user_invalid_password(client):
    """Teste para login de um usuário existente com senha inválida"""
    login_data = {
        "email": "test@example.com",
        "senha": "wrong_password"
    }
    response = client.get('/usuarios/login/', data=json.dumps(login_data),
                           content_type='application/json')
    assert response.status_code == 401
    assert 'error' in response.json
    assert response.json['error'] == 'Email, nickname ou senha incorretos'

def test_get_user(client, user_token):
    """Teste para recuperar dados de um usuário com token"""
    response = client.get('/usuarios', headers={'Authorization': f'Bearer {user_token}'})
    assert response.status_code == 200
    assert 'id' in response.json
    assert 'email' in response.json
    assert 'nickname' in response.json
    assert 'nome' in response.json
    assert 'sobrenome' in response.json

def test_update_user(client, user_token):
    response = client.put(
        '/usuarios', headers={'Authorization': f'Bearer {user_token}'},
        data=json.dumps({"nome": "Carlinhos Bala"}),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    assert 'nome' in response.json.get('atualizados')

def test_find_user_by_nickanme(client, user_token):
    response = client.get(
        '/usuarios/user1nick', headers={'Authorization': f'Bearer {user_token}'})
    assert response.status_code == 200
    assert 'id' in response.json
    assert 'email' in response.json
    assert 'nickname' in response.json
    assert 'nome' in response.json
    assert 'sobrenome' in response.json

def test_delete_user(client, user_token):
    response = client.delete(
        '/usuarios', headers={'Authorization': f'Bearer {user_token}'})
    assert response.status_code == 200
    assert 'message' in response.json
    