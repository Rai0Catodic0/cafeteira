'''modelo status'''
from user import User
from sqlalchemy import create_engine, Column, Integer, String, ForeingKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
ENGINE = create_engine('sqlite:///:memory', echo=True)
BASE = declarative_base()
SESSION = sessionmaker(bind=ENGINE)


class Status(BASE):
    '''Modelo status'''
    __tablename__ = 'cafeteira_status'
    agua_disponivel = Column(Integer)
    cafe_disponivel = Column(Integer)
    numero_de_serie = Column(String, ForeingKey(User.numero_de_serie))
