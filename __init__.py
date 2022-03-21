# init.py
# Ядро приложения, где поднимается БД, монтируется приложение
from flask import Flask 


def create_app():
    app = Flask(__name__)
    
    from .main import main
    app.register_blueprint(main)

    return app