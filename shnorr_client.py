from time import process_time_ns
import requests
import sys 
from Crypto.Util.number import getStrongPrime
import random

port = {"ca": 5001, "server": 5000}

def get_var(side, name):
    response = requests.get(f"http://127.0.0.1:{port[side]}/shnorr/{name}")
    var = response.json()[name]
    print(f"{name}:", var)
    return var


def post_var(side, name, value):
    response = requests.get(f'http://127.0.0.1:{port[side]}/shnorr/{name}/{value}')
    var = response.json()[name]
    return var


q = get_var("ca", "q")
p = get_var("ca", "p")
g = get_var("ca", "g")
t = get_var("ca", "t")

a = random.randint(1, q-1)
v = pow(g, -a, p)
print("v:", v)
id_cert = post_var("ca" ,"sign_v", v)
print("id_cert:", id_cert)
r = random.randint(1, q-1)
x = pow(g, r, p)

b = get_var("server", "b") # просим сервер забрать из са параметры

post_var("server", "cert", id_cert["cert"])
post_var("server", "id", id_cert["id"])
post_var("server", "x", x)
post_var("server", "v", v)

e = get_var("server", "e")

if e in range(1, 2**t):
    y = (a*e + r)%q
    print("-- сторона A проверяет e и отправляет y: ", y)
    verify = post_var("server", "y", y)
else:
    print("fatality")    

print("verify:", verify)