from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.String(10), primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(100), nullable=False, unique=True)
    nome = db.Column(db.String(100), nullable=False)
    sobrenome = db.Column(db.String(100), nullable=False)

class Clube(db.Model):
    __tablename__ = 'clube'
    id = db.Column(db.String(10), primary_key=True)
    criador = db.Column(db.String(10), db.ForeignKey('usuario.id'), nullable=False)
    nome = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500))

class Livro(db.Model):
    __tablename__ = 'livro'
    id = db.Column(db.String(10), primary_key=True)
    autor = db.Column(db.String(255), nullable=False)
    nome = db.Column(db.String(255), nullable=False)
    genero = db.Column(db.String(100))
    descricao = db.Column(db.String(1000))

class Participa(db.Model):
    __tablename__ = 'participa'
    usuario_id = db.Column(db.String(10), db.ForeignKey('usuario.id'), primary_key=True)
    clube_id = db.Column(db.String(10), db.ForeignKey('clube.id'), primary_key=True)

class Adiciona(db.Model):
    __tablename__ = 'adiciona'
    usuario_id = db.Column(db.String(10), db.ForeignKey('usuario.id'), primary_key=True)
    clube_id = db.Column(db.String(10), db.ForeignKey('clube.id'), primary_key=True)
    livro_id = db.Column(db.String(10), db.ForeignKey('livro.id'), primary_key=True)
    data_adicao = db.Column(db.Date, nullable=False, default=datetime.now(tz=timezone.utc))

class Avaliacao(db.Model):
    __tablename__ = 'avaliacao'
    avaliador_id = db.Column(db.String(10), db.ForeignKey('usuario.id'), primary_key=True)
    livro_id = db.Column(db.String(10), db.ForeignKey('livro.id'), primary_key=True)
    descricao = db.Column(db.String(1000))
    estrelas = db.Column(db.Integer, nullable=False)
    data_avaliacao = db.Column(db.DateTime, nullable=False, default=datetime.now(tz=timezone.utc))