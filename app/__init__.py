from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_httpauth import HTTPBasicAuth
import os

import config


app = Flask(__name__)
app.config.from_object(config.Config)
app.url_map.strict_slashes = False

db = SQLAlchemy(app)

from app.models import *

if not os.path.exists(os.path.join(config.basedir, 'app.db')):
    print("Creating the database...")
    db.create_all()

migrate = Migrate(app, db)
auth = HTTPBasicAuth()


from app.routes import *
