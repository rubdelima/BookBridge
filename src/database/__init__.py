from typing import Optional
from src.database.models import Usuario
from werkzeug.security import check_password_hash
from sqlalchemy import or_

def autenticar(senha: str, email: Optional[str] = None, nickname: Optional[str] = None) -> Usuario:
    """
    Método para retornar um usuário a partir do seu email/nickname e senha.
    
    Parâmetros de Entrada:
        - email : Optional[str] (email do usuário)
        - nickname : Optional[str] (nickname do usuário)
        - senha : str (senha do usuário)
    
    Retorno:
        Objeto da classe Usuario
    """
    
    # Realiza uma busca utilizando o email ou nickname
    user = Usuario.query.filter(
        or_(Usuario.email == email, Usuario.nickname == nickname)
    ).first()
    
    # Verifica se o usuário foi encontrado e se a senha está correta
    print(user.senha, senha, check_password_hash(user.senha, senha))
    assert user and check_password_hash(user.senha, senha)
    
    return user