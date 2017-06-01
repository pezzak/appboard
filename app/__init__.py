from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .utils import datetimefilter, nonefilter

app = Flask(__name__)
app.config.from_object('config')
app.jinja_env.filters['datetimefilter'] = datetimefilter
app.jinja_env.filters['nonefilter'] = nonefilter

db = SQLAlchemy(app)

from app import views, models
