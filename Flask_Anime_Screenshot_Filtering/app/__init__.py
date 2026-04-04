from flask import Flask
import os
from app.routes.main import main
from app.config import SECRET_KEY, UPLOAD_FOLDER, DATA_FOLDER

def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(DATA_FOLDER, exist_ok=True)

    app.register_blueprint(main)

    return app