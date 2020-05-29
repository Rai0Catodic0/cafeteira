from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
ENGINE = create_engine('sqlite:///:users.db', echo=True)
BASE = declarative_base()
Session = sessionmaker(bind=ENGINE)
session = Session()

class User(BASE):
    __tablename__ = 'users'
    _id = Column(Integer, primary_key=True)
    nome = Column(String(40),index=True)
    senha = Column(String(20))
    n_de_serie = Column(String(20), nullable=False)


    def __eq__(self, other):
        return self == other

    def autenticate(self, password):
        if password == self.senha: 
            return True
        return False

    def __repr__(self):
        return f'nome = {self.nome}, senha = {self.senha}, numero_de_serie = {self.n_de_serie}, id = {self._id}'
