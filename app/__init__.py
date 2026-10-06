from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db?timeout=30'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {'timeout': 30, 'check_same_thread': False}
}
app.config['SECRET_KEY'] = 'secret'  # for sessions

db = SQLAlchemy(app)

from app import routes, models
from flask_migrate import Migrate
migrate = Migrate(app, db)
