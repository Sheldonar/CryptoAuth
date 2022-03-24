from time import process_time_ns
import requests
import sys 
from Crypto.Util.number import getStrongPrime
import random


def get_var(name):
    response = requests.get(f"http://127.0.0.1:5000/fiat_shamir/{name}")
    var = response.json()[name]
    print(f"{name}:", var)
    return var

def post_var(name, value):
    response = requests.get(f'http://127.0.0.1:5000/fiat_shamir/{name}/{value}')
    var = response.json()[name]
    return var


N = get_var("n")

s = None
while True: # secret key
    s = getStrongPrime(1024) # ???
    if s < N-1 and N % s != 0:
        break
print("s:", s)

V = pow(s, 2, N)
print("V:", V)
post_var("v", V)
T = get_var("t")

for i in range(T):
    print("round:", i + 1)
    r = random.randint(1, N - 1)
    x = pow(r, 2, N)
    post_var("x", x)
    e = get_var("e")
    y = pow(r * pow(s, e), 1, N) 
    verify = post_var("y", y)
    print("verify:", verify)
