from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from pathlib import Path


module_path = Path(__file__).parent
templates_path = module_path.joinpath("templates")


params = {"template_folder": templates_path}

app = Flask(__name__, **params)

app.config.from_object('config')

db = SQLAlchemy(app)

from app.application.web import app_bp as application_bp

app.register_blueprint(application_bp)

db.create_all()
