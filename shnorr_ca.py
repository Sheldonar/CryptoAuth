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
from Crypto.Util.number import long_to_bytes, inverse, bytes_to_long

from flask import current_app as self

# http://127.0.0.1:5001/ - certificate authority 

shnorr_ca = Blueprint("shnorr_ca", __name__)

@shnorr_ca.route('/shnorr/q')
def generate_q():
    if not hasattr(self, 'q'):
        self.q = getStrongPrime(1024)
    print("q:", self.q)
    return json.dumps({"q": self.q})


@shnorr_ca.route('/shnorr/p')
def generate_p():
    if not hasattr(self, 'p'):
        m = 1
        self.p = 4 # не простое число для начала итерации
        while not isPrime(self.p):
            m += 1
            self.p = self.q * m + 1
    print("p:", self.p)
    return json.dumps({"p": self.p})


@shnorr_ca.route('/shnorr/t')
def generate_t():
    if not hasattr(self, 't'):
        self.t = 1
        while pow(2, self.t + 1) < self.q:
            self.t += 1
    print("t:", self.t)
    return json.dumps({"t": self.t})


@shnorr_ca.route('/shnorr/g')
def generate_g():
    if not hasattr(self, 'g'):
        self.g = 2
        while not pow(self.g, self.q, self.p) == 1:
            self.g += 1
    print("g:", self.g)
    return json.dumps({"g": self.g})


@shnorr_ca.route('/shnorr/sign_v/<val>')
def sign_v(val):
    print(1)
    if not hasattr(self, 'certs'):
        print(2)
        self.certs = []
        print(3)
    if not hasattr(self, 'pk'):
        print(4)
        self.pk = RSA.generate(1024)
        print("PK", self.pk)
        self.pub = bytes_to_long(self.pk.publickey().exportKey("PEM"))
        #self.pub = self.pk.publickey()
        print("pub", self.pub)
    print(7)
    v = int(val)
    print(8)
    id = len(self.certs)
    print(9)
    
    SHA = SHA3_512.new(long_to_bytes(id) + long_to_bytes(v))
    
    print(10)
    cert = pkcs1_15.new(self.pk).sign(SHA)
    print(11)

    pub = RSA.importKey(long_to_bytes(int(str(self.pub))))
    #pub = self.pub
    try:
        pkcs1_15.new(pub).verify(SHA, cert)
        print("УРРРРАААААА")
    except ValueError:
        print("BLET")
    self.certs.append({"v": v, "id": id, "cert":  bytes_to_long(cert)}) #идентификатор генерируем так: длина соловаря текущих сертификатов - каждый раз уникальна
    print(12)
    print("CERTS", self.certs[-1])
    return json.dumps({"sign_v": self.certs[-1]})

@shnorr_ca.route('/shnorr/pub')
def get_pub():
    print("pub:", self.pub)
    return json.dumps({"pub": self.pub})
