import os
import sqlite3
from flask import *

# Create instance
app = Flask(__name__)
app.config.from_object(__name__)

# Configuration
app.config.update(dict(
	DATABASE = os.path.join(app.root_path, 'flask.db')
	, SECRET_KEY = 'rent the key'
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# Connect to databse
def connect_db():
	db = sqlite3.connect(app.config['DATABASE'])
	db.row_factory = sqlite3.Row
	return db

