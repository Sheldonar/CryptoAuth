import sys

from Crypto import Random
from flask import Blueprint, jsonify, render_template, request
from hashlib import sha256

import json
from Crypto.Util.number import getStrongPrime, isPrime
import random

from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA3_512
from Crypto.Util.number import long_to_bytes, inverse
import requests

from flask import current_app as self

# http://127.0.0.1:5000/ - Server/client B

shnorr_server = Blueprint("shnorr_server", __name__)

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


@shnorr_server.route('/shnorr/b')
def get_b():
    self.q = get_var("ca", "q")
    self.p = get_var("ca", "p")
    self.g = get_var("ca", "g")
    self.t = get_var("ca", "t")

    self.b = random.randint(1, self.q-1)
    self.v = pow(self.g, -self.b, self.p)

    self.id_cert = post_var("ca" ,"sign_v", self.v)
    print(self.id_cert)
    return json.dumps({"b": self.id_cert["id"]})


@shnorr_server.route('/shnorr/x/<val>')
def register_x(val):
    self.x = int(val)
    return json.dumps({"x": val})


@shnorr_server.route('/shnorr/v/<val>')
def register_v(val):
    self.v = int(val)
    return json.dumps({"v": val})

@shnorr_server.route('/shnorr/cert/<val>')
def register_cert(val):
    self.cert = int(val)
    return json.dumps({"cert": val})


@shnorr_server.route('/shnorr/id/<val>')
def register_id(val):
    self.id = int(val)
    SHA = SHA3_512.new(long_to_bytes(self.id) + long_to_bytes(self.cert))
    return json.dumps({"id": val})


@shnorr_server.route('/shnorr/e')
def generate_e():
    SHA = SHA3_512.new(long_to_bytes(self.id) + long_to_bytes(self.v))
    #SHA = SHA3_512.new(b'FLAG')
    pub = RSA.importKey(long_to_bytes(int(get_var("ca", "pub"))))

    try: 
        pkcs1_15.new(pub).verify(SHA, long_to_bytes(self.cert))
        print("УРРРРАААААА")
        self.e = random.randint(1,pow(2, self.t))
        print("-- сторона B отправляет A случайное e: ", self.e)
    except ValueError as e:
        print("BLET")
        raise e
    return json.dumps({"e": self.e})


@shnorr_server.route('/shnorr/y/<val>')
def register_y(val):
    self.y = int(val)
    z = (pow(self.g, self.y, self.p)*pow(self.v, self.e, self.p))%self.p
    print(z == self.x)
    return json.dumps({"y": z == self.x})




