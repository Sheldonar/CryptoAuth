# main.py

#from random import Random, randint
import sys
from .lastrandom import LastRandom
from sqlalchemy import Integer
from Crypto import Random
from flask import Blueprint, jsonify, render_template, request
from flask_login import login_required, current_user
from hashlib import sha256

main = Blueprint('main', __name__)



@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


    