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

# Open a new database connection
def get_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

# Create database
def init_db():
	db = get_db()
	with app.open_resource('schema.sql', mode='r') as f:
		db.cursor().executescript( f.read() )
	db.commit()

# Add cmd command to initilaise the database
@app.cli.command('initdb')
def initdb_cmd():
	init_db()
	print('Initialised the database.')

# Close database
@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

#
# Views
#

@app.route('/')
def main_redirect():
	if session.get('logged_in'):
		return redirect( url_for('my_profile') )

	return redirect( url_for('login') )

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		db = get_db()
		user = request.form['username']
		password = request.form['password']
		userID = None

		# Check password
		cursor = db.execute('SELECT password, user_id FROM users WHERE username = ?', [request.form['username']])
		user = cursor.fetchone()
		if user:
			userID = user['user_id']
			if password != user['password']:
				error = 'Your password is incorrect'
			else:
				session['logged_in'] = True
				flash('Log in successful')
				return redirect( url_for('my_profile') )
		else:
			error = 'Invalid Username'
	return render_template('login.html', error=error)

# @app.route('my_profile', methods=['GET', 'POST'])
# def profile():
# 	error = None
# 	if not session.get('logged_in'):
# 		error = 'Please log in to continue.'
# 	