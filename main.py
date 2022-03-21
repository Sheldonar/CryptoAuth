# main.py
# мейн файл приложения
#from random import Random, randint
import sys

from Crypto import Random
from flask import Blueprint, jsonify, render_template, request
from hashlib import sha256

import json
from Crypto.Util.number import getStrongPrime
import random

from flask import current_app as self

main = Blueprint("main", __name__)


@main.route('/n')
def generate_n():
    self.p = getStrongPrime(1024)
    self.q = getStrongPrime(1024)
    self.N = self.p * self.q
    print("N:", self.N)
    return json.dumps({"n": self.N})

@main.route('/v/<val>')
def register_v(val):
    self.V = int(val)
    return json.dumps({"v": self.V})


@main.route('/t')
def generate_t():
    t = random.randint(5, 10)
    print("t:", t)
    return json.dumps({"t": t})


@main.route('/x/<val>')
def register_x(val):
    self.x = int(val)
    return json.dumps({"x": self.x})


@main.route('/e')
def generate_e():
    self.e = random.choice([0, 1])
    print("e:", self.e)
    return json.dumps({"e": self.e})


@main.route('/y/<val>') 
def verify(val):
    self.y = int(val)
    verify = pow(self.y, 2, self.N) == pow(self.x * pow(self.V, self.e), 1, self.N)
    return json.dumps({"y": verify})  
