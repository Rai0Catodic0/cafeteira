'''rotas do site e api '''
from json import loads
from jinja2 import Environment, PackageLoader, select_autoescape
from bottle import default_app, route, static_file, request
import core
from requests import get
ENV = Environment(
    loader=PackageLoader('mysite', 'views'),
    autoescape=select_autoescape(['html', 'xml'])
)


@route('/')
def hello_world():
    ''' rota da pagina inicial '''
    return static_file('index.html', root='mysite/views')


@route('/singin')
def singin():
    ''' rota para a pagina login '''
    return static_file('cadastro.html', root='mysite/views')


@route('/adduser', method='POST')
def cadastro():
    ''' link do cadastro'''
    user = {'name':request.forms.get('name'),
            'password' : request.forms.get('password'),
            'n_de_serie': request.forms.get('n_de_serie')}
    core.insert_user(user)
    return static_file('cadastro.html', root='mysite/views')

@route('/result', method='POST')
def do_login():
    '''link do botao de login'''
    username = request.forms.get('val1')
    password = request.forms.get('val2')
    x = core.autenticate(username, password)
    n = core.get_serial(password)
#    print(n)
    template = ENV.get_template('painel.html')
    task = core.get_task(n[0])
    _id = request.forms.get('id')
    if x == True:
        return template.render(tasks=task)
    else:
        return "<p>senha errada</p>"


@route('/home', method='GET')
def home():
    '''rota para a home'''
    return static_file('home.html', root='mysite/views')



@route('/painel1', method='POST')
def delete_p():
    '''deleta uma tarefa'''
    _id = request.forms.get('id')
    core.delete(_id)
    template = ENV.get_template('painel.html')
    task = core.get_task('2203')
    return template.render(tasks=task)


@route('/api_hora')
def hora():
    ''' retorna o horario para a cafeteira'''
    Hora = get('http://worldtimeapi.org/api/America/Sao_Paulo').text
    Hora = loads(Hora)
    Hora = Hora['datetime']
    Hora = Hora.split('T')
    Hora = Hora.pop(1)
    Hora = Hora.split('.')
    Hora = Hora.pop(0)
    return Hora


@route('/api_task')
def return_task():
    '''retorna as tarefas para a cafeteira'''
    n_de_serie = request.headers.get('n')
    n = request.headers.get('y')
    if n_de_serie == '':
        return 'erro', n
    else:
#        n = int(n)
        x = core.get_task(n_de_serie)
#        tasks.append(str(x[n_de_serie]))
        return x


@route('/task')
def task():
    '''rota para a pagina com as tarefas'''
    return static_file('taskinator.html', root='mysite/views')


@route('/add_task', method='POST')
def add_task():
    '''Adiciona a tarefa'''
    task = {'cafe': request.forms.get('cafe'),
            'agua': request.forms.get('agua'),
            'horario': request.forms.get('horario'),
            'nome': request.forms.get('nome'),
            'n_de_serie':'2203'}
    x = core.insert_task(task)
    if x is True:
        return 'tarefa adicionada com sucesso'


@route('/teste')
def teste():
    '''rota de teste'''
    x = request.headers.get('hora')
    positivo = core.insert_teste(x)
    return str(positivo)


@route('/horarios')
def debug():
    '''confirma que a tarefa foi concluida'''
    Horarios = core.get_teste()
    template = ENV.get_template('debug.html')
    return template.render(horarios=Horarios)

APPLICATION = default_app()
