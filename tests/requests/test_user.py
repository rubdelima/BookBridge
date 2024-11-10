import pytest
import json

@pytest.fixture
def new_user_data():
    return {
        "email": "test@example.com",
        "senha": "Senha@123",
        "nickname": "testuser",
        "nome": "Test",
        "sobrenome": "User"
    }

def test_create_user(client, new_user_data):
    """Teste para criação de um novo usuário"""
    response = client.post('/usuarios', data=json.dumps(new_user_data), content_type='application/json')
    assert response.status_code == 200 
    assert 'token' in response.json
