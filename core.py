from sqlalchemy import (create_engine, MetaData, Column,
                        Table, Integer, String, select, update, ForeignKey)
import json

engine = create_engine('sqlite:///teste.db', echo=False)

metadata = MetaData(bind=engine)

users = Table('usuarios', metadata,
              Column('id', Integer, primary_key=True),
              Column('nome', String(40), index=True),
              Column('senha', String),
              Column('numero_de_serie', String,  nullable=False))
cafeteira_status = Table('Cafeteira_status', metadata,
                         Column('agua_disponivel', Integer),
                         Column('cafe_disponivel', Integer),
                         Column('n_de_serie', String,
                                ForeignKey(users.c.numero_de_serie)))
cafeteira_tasks = Table('Cafeteira_tasks', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('cafe', Integer, nullable=False),
                        Column('agua', Integer, nullable=False),
                        Column('horario', String, nullable=False),
                        Column('n_de_serie', String,
                               ForeignKey(users.c.numero_de_serie)))
teste = Table('horario',metadata,
               Column('id', Integer, primary_key=True),
               Column('hora',String))

# metadata.create_all()

def Update(status):
    stmt = update(cafeteira_status).where(cafeteira_status.c.n_de_serie==status['n_de_serie']).values(cafe_disponivel=status['cafe_disponivel']).execute()
    return True


def insert_status(status):
    conn = engine.connect()
    status['n_de_serie'] = select([users.c.numero_de_serie]).where(users.c.nome == status['nome'])
    cafeteira = cafeteira_status.insert()
    Status = cafeteira.values(cafe_disponivel=status['cafe_disponivel'],
                              agua_disponivel=status['agua_disponivel'],
                              n_de_serie=status['n_de_serie'])
    print(status)
    conn.execute(Status)
    conn.close()
    return True


def insert_task(settings):
    n_de_serie = select([users.c.numero_de_serie]).where(users.c.nome == settings['nome'])
    for row in n_de_serie.execute():
        print(row)
        settings['n_de_serie']=row[0]
    conn = engine.connect()
    cafeteira = cafeteira_tasks.insert()
    new_task = cafeteira.values(cafe=settings['cafe'],
                                agua=settings['agua'],
                                horario=settings['horario'],
                                n_de_serie=settings['n_de_serie'])
    print(settings)
    conn.execute(new_task)
    conn.close
    return True


def insert_user(user):
    conn = engine.connect()
    user_ins = users.insert()
    new_user = user_ins.values(nome=user['name'], senha=user['password'],
                               numero_de_serie=user['n_de_serie'])
    print(user)
    conn.execute(new_user)
    conn.close()
    return True


def autenticate(nome, senha):
    user = select([users.c.senha]).where(users.c.nome == nome)
    for x in user.execute():
        if x[0] == senha:
            return True
        else:
            return False
def get_task(N_de_serie):
    data = select([cafeteira_tasks.c.id,
                   cafeteira_tasks.c.agua,
                   cafeteira_tasks.c.cafe,
                   cafeteira_tasks.c.horario,
                   cafeteira_tasks.c.n_de_serie]).where(cafeteira_tasks.c.n_de_serie == N_de_serie).execute()
    task =  {_id:{'id': _id,"cafe":cafe,
                        "agua":agua,
                        "horario":horario,
                        "n_de_serie":n_de_serie}
            for _id,agua,cafe,horario,n_de_serie in data}
    return task
def insert_teste(Hora):
    conn = engine.connect()
    teste_insert= teste.insert()
    novo_horario = teste_insert.values(hora=Hora)
    print(Hora)
    conn.execute(novo_horario)
    conn.close()
    return Hora
def get_teste():
    x = select([teste])
    lista = [ i for i in x.execute()]
    return lista


def delete(_id):
    Del = cafeteira_tasks.delete().where(cafeteira_tasks.c.id == _id)
    Del.execute()
    return True


def get_serial(password):
    query = select([users.c.numero_de_serie]).where(users.c.senha == password)
    for i in query.execute():
        return i

