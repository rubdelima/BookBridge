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
    