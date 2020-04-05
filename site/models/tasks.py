from sqlalchemy import create_engine, Column, Integer, String, ForeingKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
ENGINE = create_engine('sqlite:///:memory', echo=True)
BASE = declarative_base()
SESSION = sessionmaker(bind=ENGINE)


class Tasks(BASE):
    '''Modelo das tarefas'''
    __tablename__ = 'Tasks'
    _id = Column(Integer, primary_key=True)
    cafe = Column(Integer, nullable=False)
    agua = Column(Integer, nullable=False)
    horario = Column(String, nullable=False)
