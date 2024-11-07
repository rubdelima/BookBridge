from pydantic import BaseModel, constr
from typing import Annotated, Optional

class UsuarioValidacao(BaseModel):
    "Classe do usuário no Banco de Dados"
    
    id : str
    "Id único do usuário, chave primária que referencia o usuário"
    
    email : str
    "Email utilizado pelo usuário, deve ter um valor não nulo e pode ser alterado"
    
    senha : Annotated[str, constr(pattern=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$')]
    "Senha do usuário, deve conter no mínimo 8 caracteres, dentre eles deva haver ao menos uma letra maúscula, uma minúscula e uma letra"
    
    nickname : str
    "Nickname que referencia o usuário, ela é única e exclusiva a esse usuário"
    
    nome : str
    "Nome do Usuário"
    
    sobrenome : str
    "Sobrenome do Usuário"
    
class ClubeValidacao(BaseModel):
    "Modelo de um Clube de Livros no Banco de Dados"
    
    id : str
    "Identificação única do clube "
    
    criador : str
    "Id que referencia o usuário que criou o clube"
    
    nome : str
    "Nome o qual o Clube é chamado e pode ser buscado pelo usuário"
    
    description : str
    "Descrição do Clube"

class LivroValidacao(BaseModel):
    "Modelo de um livro no Banco de Dados"
    
    id : str
    "Identificaçao única do Livro"
    
    autor : str
    "Nome do autor que fez o livro, pode ser importante para buscas"
    
    nome : str
    "Nome do livro"
    
    genero : Optional[str] = None
    "Genero no qual esse livro pertence, pode ser utilizado como parâmetro de busca"
    
    descricao : Optional[str] = None
    "Descrição do livro em questao"
    
class AvaliacaoValidacao(BaseModel):
    "Modelo de uma avaliação no Banco de Dados"
    avaliador_id :str
    "Identificação de quem realizou a avaliação"
    
    livro_id : str
    "Identificação do livro"
    
    descricao : Optional[str] = None
    "Texto da avaliação"

    estrelas : int
    "Quantidade de estrelas dadas a um determinado livro, varia entre 0 e 5"    