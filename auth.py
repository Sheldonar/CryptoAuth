# auth.py

from http import server
from logging import lastResort
from tabnanny import check
from flask import Blueprint, jsonify, render_template, redirect, url_for, request, flash
from hashlib import sha256
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db
from .lastrandom import LastRandom
from Crypto import Random

auth = Blueprint('auth', __name__)

def check_pap (saved_password, input_password_hash): # PAP 
    saved_password_hash = sha256(bytes(saved_password, encoding = "utf-8")).digest().hex()
    print(saved_password)
    print(saved_password_hash)
    print(input_password_hash)
    return saved_password_hash == input_password_hash

def check_chap (saved_password, input_password_hash): # CPAP 1-side and 2 side
    saved_password_hash = sha256(bytes(LastRandom.N + saved_password, encoding = "utf-8")).digest().hex()
    print(saved_password)
    print(saved_password_hash)
    print(input_password_hash)
    return saved_password_hash == input_password_hash

def check_skey (saved_password, input_password_hash): # S/Key
    saved_password_hash = skey_password(saved_password, LastRandom.s_key_N)
    input_password_hash = skey_password(input_password_hash, LastRandom.I)
    print(saved_password)
    print(saved_password_hash)
    print(input_password_hash)
    return saved_password_hash == input_password_hash

def skey_password(password, I):
    password_hash = password
    print (password)
    print (I)
    for i in range(0, I):
        password_hash = sha256(bytes(password_hash, encoding = "utf-8")).digest().hex()
        print (str(i) + " " + password_hash)
    return password_hash

@auth.route('/login')
def login():
    return render_template('login.html', server_password = LastRandom.server_password) # пароль для сервера

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    method = request.form.get('authmethod')
    user = User.query.filter_by(email=email).first()
    if not user: 
        flash('No such User')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    remember = True # if request.form.get('remember') else False
    print(method)
    
    check = False
    if method == "PAP":
        check = check_pap(user.password, password)
    elif method in {"CHAP1", "CHAP2"}:
        check = check_chap(user.password, password)
    elif method in {"SKEY"}:
        check = check_skey(user.password, password)    
    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not check:
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again  
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=password)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/rand', methods=['GET'])
def get_rand_num():
    # GET request
    LastRandom.N = str(Random.get_random_bytes(128))
    message = {'N': LastRandom.N} #  максимальное число размером 128 bytes
    return jsonify(message)  # serialize and use JSON headers
    
@auth.route('/chap2', methods=['POST'])
def get_chap2_rand_num():
    # GET request
    LastRandom.N = str(Random.get_random_bytes(128))
    M = request.get_json()["M"]
    message = {'N': LastRandom.N, 'password_hash': sha256(bytes(M + LastRandom.server_password, encoding = "utf-8")).digest().hex()} #  максимальное число размером 128 bytes
    print(message ['password_hash'])
    print(M)
    return jsonify(message)  # serialize and use JSON headers

@auth.route('/skey', methods=['GET'])
def get_skey_I():
    # GET request
    LastRandom.I = LastRandom.I + 1
    message = {'I': LastRandom.I, 'N': LastRandom.s_key_N} 
    return jsonify(message)  # serialize and use JSON headers