# init.py
# Ядро приложения, где поднимается БД, монтируется приложение
from flask import Flask 


def create_app():
    app = Flask(__name__)
    
    from .fiat_shamir_server import fiat_shamir
    app.register_blueprint(fiat_shamir)


    from .shnorr_server import shnorr_server
    app.register_blueprint(shnorr_server)


    from .shnorr_ca import shnorr_ca
    app.register_blueprint(shnorr_ca)

    return app