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
		return redirect( url_for('profile') )

	return redirect( url_for('login') )

@app.route('/login', methods=['GET', 'POST'])
def login():
	if session.get('logged_in'):
		return redirect( url_for('profile') )
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
				session['userID'] = userID
				flash('Log in successful')
				return redirect( url_for('profile') )
		else:
			error = 'Invalid Username'
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect( url_for('login') )

@app.route('/profile', methods=['GET', 'POST'])
def profile():
	error = None
	user = None
	if not session.get('logged_in'):
		error = 'Please log in to continue.'
		return render_template('login.html', user=user, error=error)

	# we only need a simple message
	db = get_db()
	cursor = db.execute('SELECT * FROM users_info WHERE user_id = ?', str(session.get('userID')) )
	user = cursor.fetchone()
	return render_template('profile.html', user=user, error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
	error = None
	db = get_db()

	if request.method == 'POST':
		username = request.form['username'].strip()
		password = request.form['password'].strip()
		nickname = request.form['nickname'].strip()

		result = db.execute('SELECT username FROM users').fetchall();
		allUsers = [u['username'] for u in result]

		if username == '':
			error = 'Username cannot be blank.'
		elif username in allUsers:
			error = 'Sorry, username already exsits'
		elif len(password) < 4:
			error = 'Your password must have at least 4 characters.'
		elif nickname == '':
			error = 'You need to have a nickname.'
		else:
			cursor = db.cursor()
			cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', [username, password])
			user_id = cursor.lastrowid
			cursor.execute('INSERT INTO users_info (user_id, nickname) VALUES (?, ?)', [user_id, nickname])
			db.commit()
			flash('You are now registered. Please log in to continue')
			return redirect( url_for('login') )
	return render_template('register.html', error=error)

@app.route('/database')
def database():
	error = None
	db = get_db()
	users = db.execute('SELECT * FROM users')
	return render_template('database.html', error=error, users=users)