from bottle import default_app, route, static_file,request
from time import strftime
import core
from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader('mysite', 'views'),
    autoescape=select_autoescape(['html', 'xml'])
)


from requests import get
from json import loads


@route('/')
def hello_world():
#    return output
    return static_file('index.html', root='mysite/views')


@route('/singin')
def singin():
    return static_file('cadastro.html',root='mysite/views')


@route('/adduser', method='POST')
def cadastro():
    user = {'name':request.forms.get('name'),
            'password' : request.forms.get('password'),
            'n_de_serie': request.forms.get('n_de_serie')}
    core.insert_user(user)
    return static_file('cadastro.html',root='mysite/views')

@route('/result', method='POST')
def do_login():
    username = request.forms.get('val1')
    password = request.forms.get('val2')
    x=core.autenticate(username,password)
    n = core.get_serial(password)
    print(x)
#    print(n)
    template = env.get_template('painel.html')
    task = core.get_task(n[0])
    _id = request.forms.get('id')
    if x == True:
        return template.render(tasks=task)
    else:
        return "<p>senha errada</p>"

@route('/home',method='GET')
def home():
        return static_file('home.html', root='mysite/views')



@route('/painel1', method='POST')
def delete_p():
    _id = request.forms.get('id')
    core.delete(_id)
    template = env.get_template('painel.html')
    task = core.get_task('2203')
    return template.render(tasks=task)
@route('/api_hora')
def hora():
    hora = get('http://worldtimeapi.org/api/America/Sao_Paulo').text
    hora= loads(hora)
    hora = hora['datetime']
    hora = hora.split('T')
    hora = hora.pop(1)
    hora = hora.split('.')
    hora = hora.pop(0)
    return hora
@route('/api_task')
def return_task():
    tasks=[]
    n_de_serie =request.headers.get('n')
    n= request.headers.get('y')
    if n_de_serie == '':
        return 'erro',n
    else:
#        n = int(n)
        x= core.get_task(n_de_serie)
#        tasks.append(str(x[n_de_serie]))
        return x


@route('/task')
def task():
    return static_file('taskinator.html', root='mysite/views')
@route('/add_task', method='POST')
def add_task():
    task  = {'cafe': request.forms.get('cafe'),
             'agua': request.forms.get('agua'),
             'horario': request.forms.get('horario'),
             'nome': request.forms.get('nome'),
             'n_de_serie':'2203'}
    x = core.insert_task(task)
    if x is True:
        return 'tarefa adicionada com sucesso'
    else:
        return 'erro'


@route('/teste')
def teste():
    x = request.headers.get('hora')
    positivo = core.insert_teste(x)
    return str(positivo)


@route('/horarios')
def debug():
    Horarios = core.get_teste()
    template = env.get_template('debug.html')
    return template.render(horarios=Horarios)

application = default_app()
