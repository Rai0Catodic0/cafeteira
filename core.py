'''operacoes do banco de dados'''
from sqlalchemy import (create_ENGINE, MetaData, Column,
                        Table, Integer, String, select, update, ForeignKey)

ENGINE = create_ENGINE('sqlite:///TESTE.db', echo=False)

METADATA = MetaData(bind=ENGINE)

USERS = Table('usuarios', METADATA,
              Column('id', Integer, primary_key=True),
              Column('nome', String(40), index=True),
              Column('senha', String),
              Column('numero_de_serie', String, nullable=False))
CAFETEIRA_STATUS = Table('Cafeteira_status', METADATA,
                         Column('agua_disponivel', Integer),
                         Column('cafe_disponivel', Integer),
                         Column('n_de_serie', String,
                                ForeignKey(USERS.c.numero_de_serie)))
CAFETEIRA_TASKS = Table('Cafeteira_tasks', METADATA,
                        Column('id', Integer, primary_key=True),
                        Column('cafe', Integer, nullable=False),
                        Column('agua', Integer, nullable=False),
                        Column('horario', String, nullable=False),
                        Column('n_de_serie', String,
                               ForeignKey(USERS.c.numero_de_serie)))
TESTE = Table('horario', METADATA,
              Column('id', Integer, primary_key=True),
              Column('hora', String))

# METADATA.create_all()

def Update(status):
    '''Opercao de update'''
    stmt = update(CAFETEIRA_STATUS).where(CAFETEIRA_STATUS.c.n_de_serie == status['n_de_serie']).values(cafe_disponivel=status['cafe_disponivel']).execute()
    return True


def insert_status(status):
    '''opercao insert'''
    conn = ENGINE.connect()
    status['n_de_serie'] = select([USERS.c.numero_de_serie]).where(USERS.c.nome == status['nome'])
    cafeteira = CAFETEIRA_STATUS.insert()
    status = cafeteira.values(cafe_disponivel=status['cafe_disponivel'],
                              agua_disponivel=status['agua_disponivel'],
                              n_de_serie=status['n_de_serie'])
    print(status)
    conn.execute(status)
    conn.close()
    return True


def insert_task(settings):
    '''opercao insert'''
    n_de_serie = select([USERS.c.numero_de_serie]).where(USERS.c.nome == settings['nome'])
    for row in n_de_serie.execute():
        print(row)
        settings['n_de_serie'] = row[0]
    conn = ENGINE.connect()
    cafeteira = CAFETEIRA_TASKS.insert()
    new_task = cafeteira.values(cafe=settings['cafe'],
                                agua=settings['agua'],
                                horario=settings['horario'],
                                n_de_serie=settings['n_de_serie'])
    print(settings)
    conn.execute(new_task)
    conn.close()
    return True


def insert_user(user):
    '''opercao insert'''
    conn = ENGINE.connect()
    user_ins = USERS.insert()
    new_user = user_ins.values(nome=user['name'], senha=user['password'],
                               numero_de_serie=user['n_de_serie'])
    print(user)
    conn.execute(new_user)
    conn.close()
    return True


def autenticate(nome, senha):
    '''select pra comparacao de login'''
    user = select([USERS.c.senha]).where(USERS.c.nome == nome)
    for x in user.execute():
        if x[0] == senha:
            return True
        else:
            return False
def get_task(N_de_serie):
    '''select que retorna tarefas'''
    data = select([CAFETEIRA_TASKS.c.id,
                   CAFETEIRA_TASKS.c.agua,
                   CAFETEIRA_TASKS.c.cafe,
                   CAFETEIRA_TASKS.c.horario,
                   CAFETEIRA_TASKS.c.n_de_serie]).where(CAFETEIRA_TASKS.c.n_de_serie == N_de_serie).execute()
    task = {_id:{'id': _id, "cafe":cafe,
                 "agua":agua,
                 "horario":horario,
                 "n_de_serie":n_de_serie}
            for _id, agua, cafe, horario, n_de_serie in data}
    return task
def insert_teste(hora):
    '''opercao insert'''
    conn = ENGINE.connect()
    teste_insert = TESTE.insert()
    novo_horario = teste_insert.values(hora=hora)
    print(hora)
    conn.execute(novo_horario)
    conn.close()
    return hora
def get_teste():
    '''teste'''
    x = select([TESTE])
    lista = [i for i in x.execute()]
    return lista


def delete(_id):
    '''delete'''
    dele = CAFETEIRA_TASKS.delete().where(CAFETEIRA_TASKS.c.id == _id)
    dele.execute()
    return True


def get_serial(password):
    '''retorna o numero de serie'''
    query = select([USERS.c.numero_de_serie]).where(USERS.c.senha == password)
    for i in query.execute():
        return i
