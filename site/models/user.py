from sqlalchemy import create_engine, Column, Integer, String, ForeingKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
ENGINE = create_engine('sqlite:///:memory', echo=True)
BASE = declarative_base()
SESSION = sessionmaker(bind=ENGINE)

class User(BASE):
    __tablename__ = 'users'
    _id = Column(Integer, primary_key=True)
    nome = Column(String(40),index=True)
    senha = Column(String)
    numero_de_serie = Column(String, nullable=False)


    def __repr__(self):
        return f'nome = {self.nome}, senha = {self.senha}, numero_de_serie = {self.numero_de_serie}, id = {self._id}'
