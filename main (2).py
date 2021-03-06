from machine import PWM,Pin
from utime import sleep
import time
from machine import Pin, PWM, RTC
from time import sleep
from urequests import get
import ujson as json


def time_to_int(t):
    return t[0]*3600 + t[1]*60 + t[2]


def str_to_time(string,seg):
lista  = string.split(':')
    for i in range(len(lista)):
        lista[i]=int(lista[i])
        if seg is True:
            time = lista[0]*3600+lista[1]*60+lista[2]
            return time
        else:
            return lista


def decorador(f):
    def sched(t1, t2,value):
        while True:
            t = time.localtime()
            current_time = time_to_int((t[3], t[4], t[5]))
            if current_time >= t1 and current_time <= t2:
                print('funcao ok')
                return f(t1, t2,value)
            else:
                #rele.value(1)
                print('passou')
                print(current_time)
                sleep(0.5)
            return sched


def get_task():
    headers = {'n': '2203', 'y': '1'}
    url = 'http://raiocatodic0.pythonanywhere.com/api_task'
    result = get(url, headers=headers).text
    print(result)
    result = json.loads(result)
    return result


def retorna_hora():
    header = {'hora': str(rtc.datetime())}
    hora = get('http://raiocatodic0.pythonanywhere.com/teste', headers=header).text
    return hora


def colocar_agua(ml):
    t = ml/5
    p = Pin(5, Pin.OUT)
    p.value(0)
    sleep(t)
    p.value(1)
    return True


def cafe(Cafe):
    while Cafe >0 :
        servo = PWM(Pin(2, Pin.OUT), freq=50)
        servo.duty(115)
        sleep(2)
        servo.duty(25)
        sleep(2)
        Cafe -=1
        return True
#@decorador
def fazer_cafe(t1,t2, agua):
    cafeteira = Pin(4, Pin.OUT)
    cafeteira.value(1)
    #parametros = result
    #print(parametros)
    print('agua')
    colocar_agua(agua['agua'])
    print('cafe')
    cafe(agua['cafe'])
    cafeteira.value(0)
    print('agua+cafe')
    sleep(240)
    cafeteira.value(1)
    return True


rtc = machine.RTC()
hora = get('http://raiocatodic0.pythonanywhere.com/api_hora').text
Hora = str_to_time(hora, 0)rtc.datetime((2019, 7, 31, 0, Hora[0], Hora[1], Hora[2], 0))
headers = {'n': '2203', 'y': '1'}
url = 'http://raiocatodic0.pythonanywhere.com/api_task'
result = get(url, headers=headers).textprint(result)
result = json.loads(result)
#dic = {'horario':'17:24:00',  'agua':200,'CAfe':2}
#t=str_to_time(dic['horario'],True)t2=t+20
#fazer_cafe(t,t2,dic)
dic = get_task()
x = list(dic.keys())
for i in range(len(x)):
    print(x[i])
    print('agua',dic[x[i]]['agua'])
    print('cafe',dic[x[i]]['cafe'])
    fazer_cafe(1,1,dic[x[i]])
