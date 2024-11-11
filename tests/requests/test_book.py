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

def test_post_livro(client, user_token):
    response = client.post(
        '/livros', data=json.dumps({
            "nome": "Quincas Borba",
            "autor": "Machado de Assis",
            "genero": "Romance",
            "descricao": "O romance a ascensão social de Rubião que, após receber toda a herança do filósofo louco Quincas Borba - criador da filosofia Humanitas e muda-se para a ..."
        }),
        headers={'Authorization': f'Bearer {user_token}'},
        content_type='application/json'
    )
    
    assert response.status_code == 201
    assert 'message' in response.json
    assert response.json['message'] == 'Livro criado com sucesso'

def test_get_livro(client):
    response = client.get('/livros/L019')
    assert response.status_code == 200
    assert response.json['livro'].get('nome') == "O Cortiço"
    assert response.json['livro'].get('autor') == "Aluísio Azevedo"
    assert response.json['livro'].get('genero') == "Naturalismo"
    assert 'descricao' in response.json['livro'].keys()

def test_get_livros_por_autor(client):
    response = client.get('/livros/buscar?autor=Machado de Assis')
    assert response.status_code == 200
    assert len(response.json['livros']) > 1

def test_post_avaliacao(client, user_token):
    response = client.post(
        '/livros/avaliar',
        data=json.dumps({
            "livro_id": "L019",
            "estrelas": 5,
            "descricao": "Muito bom!"
        }),
        headers={'Authorization': f'Bearer {user_token}'},
        content_type='application/json'
    )
    
    assert response.status_code == 201
    assert 'message' in response.json
    assert response.json['message'] == 'Avaliação realizada com sucesso'
