from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

app = Flask(
    __name__, 
    template_folder='templates',
    static_folder='statics')
app.config.from_object(Config)

db = SQLAlchemy(app)

from .routes import generales
from .routes import insertions
from .routes import suppression
from .routes import update
from .routes import recherche
from .routes import erreurs