# Documentação de Banco de Dados

## Modelos e Entidades

### Usuario
Representa os usuários cadastrados na aplicação. Os atributos são:
- `id`: VARCHAR2(10), chave primária.
- `email`: VARCHAR2, obrigatório.
- `senha`: VARCHAR2, obrigatório.
- `nickname`: VARCHAR2, obrigatório.
- `nome`: VARCHAR2, obrigatório.
- `sobrenome`: VARCHAR2, obrigatório.

### Clube
Representa um clube de leitura criado por um usuário. Os atributos são:
- `id`: VARCHAR2, chave primária.
- `criador`: VARCHAR2, chave estrangeira referenciando `Usuario`.
- `nome`: VARCHAR2, obrigatório.
- `description`: VARCHAR2, opcional.

### Livro
Representa os livros que podem ser adicionados aos clubes de leitura. Os atributos são:
- `id`: VARCHAR2, chave primária.
- `autor`: VARCHAR2, obrigatório.
- `nome`: VARCHAR2, obrigatório.
- `genero`: VARCHAR2, opcional.

### Avaliacao
Representa uma avaliação feita por um usuário sobre um livro. Os atributos são:
- `id`: VARCHAR2, chave primária.
- `avaliador`: VARCHAR2, chave estrangeira referenciando `Usuario`.
- `livro`: VARCHAR2, chave estrangeira referenciando `Livro`.
- `descricao`: VARCHAR2, opcional.
- `estrelas`: INTEGER, intervalo de 0 a 5, obrigatório.
- `data_avaliacao`: DATETIME, obrigatório.

## Relações

### Criar Clube
**Tipo**: Relação (1:N) entre `Usuario` e `Clube`.

**Descrição**: Um usuário pode criar vários clubes de leitura, mas cada clube tem um único criador.

### Participar de Clube
**Tipo**: Relação (N:N) entre `Usuario` e `Clube`.

**Descrição**: Um usuário pode participar de vários clubes de leitura, e um clube pode ter múltiplos usuários.

### Adicionar Livro
**Tipo**: Relação (N:N:N) entre `Usuario`, `Clube` e `Livro`.

**Descrição**: Um usuário pode adicionar vários livros em diferentes clubes, mas um mesmo livro só pode ser adicionado uma vez em um clube.

### Avaliar
**Tipo**: Relação (N:N) entre `Usuario` e `Livro`.

**Descrição**: Um usuário pode avaliar um livro, e um livro pode ser avaliado por vários usuários.

## Diagrama ER
```mermaid
---
title: Database Schema
---
erDiagram
    
USUARIO {
    VARCHAR2(10) id
    VARCHAR2 email
    VARCHAR2 senha
    VARCHAR2 nickname
    VARCHAR2 nome
    VARCHAR2 sobrenome
}

CLUBE {
    VARCHAR2 id
    VARCHAR2 criador
    VARCHAR2 nome
    VARCHAR2 description
}

LIVRO {
    VARCHAR2 id
    VARCHAR2 autor
    VARCHAR2 nome
    VARCHAR2 genero
    VARCHAR2 descricao
}

PARTICIPA {
    VARCHAR2 usuario_id
    VARCHAR2 clube_id
}

ADICIONAR {
    VARCHAR2 usuario_id
    VARCHAR2 clube_id
    VARCHAR2 livro_id
    DATE data_adicao
}

AVALIAR {
    VARCHAR2 avaliador_id
    VARCHAR2 livro_id
    VARCHAR2 descricao
    INTEGER nota
    DATE data_avaliacao
}

USUARIO ||--o{ CLUBE : "cria"
USUARIO }o--o{ PARTICIPA : "participa"
CLUBE }o--o{ PARTICIPA : "tem membro"
USUARIO }o--o{ ADICIONAR : "adiciona"
CLUBE }o--o{ ADICIONAR : "contém"
LIVRO }o--o{ ADICIONAR : "inclui"
USUARIO }o--o{ AVALIAR : "faz"
LIVRO }o--o{ AVALIAR : "é avaliado"