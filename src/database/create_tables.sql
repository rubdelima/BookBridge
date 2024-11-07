CREATE TABLE Usuario (
    id VARCHAR2(10) PRIMARY KEY,
    email VARCHAR2(255) NOT NULL UNIQUE,
    senha VARCHAR2(255) NOT NULL,
    nickname VARCHAR2(100) NOT NULL UNIQUE,
    nome VARCHAR2(100) NOT NULL,
    sobrenome VARCHAR2(100) NOT NULL
);

CREATE TABLE Clube (
    id VARCHAR2(10) PRIMARY KEY,
    criador VARCHAR2(10),
    nome VARCHAR2(255) NOT NULL,
    description VARCHAR2(500),
    FOREIGN KEY (criador) REFERENCES Usuario(id)
);

CREATE TABLE Livro (
    id VARCHAR2(10) PRIMARY KEY,
    autor VARCHAR2(255) NOT NULL,
    nome VARCHAR2(255) NOT NULL,
    genero VARCHAR2(100),
    descricao VARCHAR2(500)
);

CREATE TABLE Participa (
    usuario_id VARCHAR2(10),
    clube_id VARCHAR2(10),
    PRIMARY KEY (usuario_id, clube_id),
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id),
    FOREIGN KEY (clube_id) REFERENCES Clube(id)
);

CREATE TABLE Adiciona (
    usuario_id VARCHAR2(10),
    clube_id VARCHAR2(10),
    livro_id VARCHAR2(10),
    data_adicao DATE NOT NULL,
    PRIMARY KEY (usuario_id, clube_id, livro_id),
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id),
    FOREIGN KEY (clube_id) REFERENCES Clube(id),
    FOREIGN KEY (livro_id) REFERENCES Livro(id)
);

CREATE TABLE Avaliacao (
    avaliador_id VARCHAR2(10) NOT NULL,
    livro_id VARCHAR2(10) NOT NULL,
    descricao VARCHAR2(1000),
    estrelas INTEGER CHECK (estrelas BETWEEN 0 AND 5),
    data_avaliacao DATETIME NOT NULL,
    PRIMARY KEY (avaliador_id, livro_id),
    FOREIGN KEY (avaliador) REFERENCES Usuario(id),
    FOREIGN KEY (livro) REFERENCES Livro(id)
);
