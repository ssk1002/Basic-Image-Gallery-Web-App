#Some code used from http://code.runnable.com/UiPcaBXaxGNYAAAL/how-to-upload-a-file-to-the-server-in-flask-for-python


#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import hashlib
import pymysql.cursors
import datetime
from werkzeug import secure_filename
import os
import datetime
from math import ceil

#Initialize the app from Flask
app = Flask(__name__)

UPLOAD_FOLDER = './static/images/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure MySQL
conn = pymysql.connect( unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock',
 					    host='localhost',
						user='root',
						password='root',
						db='image-gallery',
						charset='utf8mb4',
						cursorclass=pymysql.cursors.DictCursor)
				
#Define route for landing at /
@app.route('/')
def landing():
	return redirect(url_for('home'))
	
#Define route for landing at home
@app.route('/home', defaults={'page':1}, methods=['GET', 'POST'])
@app.route('/home<int:page>', methods=['GET', 'POST'])
def home(page):
	print 'hello!!!!'
	perpage = 10
	startat = ((page - 1) * perpage)
	cursor = conn.cursor()
	query = 'SELECT COUNT(*) as ct FROM pictures'
	cursor.execute(query)
	data = cursor.fetchone()
	totalpages = int(ceil( data['ct'] / 10.0 ))
	if totalpages == 0:
		totalpages = 1
	query = 'SELECT * FROM `pictures` ORDER BY `pictures`.`time` ASC limit %s, %s'
	cursor.execute(query, (startat, perpage))
	data = cursor.fetchall()
	print data
	if session.get('logged_in') is True:
		return render_template('home.html', logged_in = True, username = session['username'], page = page, lastpage = totalpages, pictures = data)
	return render_template('home.html', page = page, lastpage = totalpages, pictures = data)

#def home():
	#SELECT * FROM `pictures` ORDER BY `pictures`.`time` ASC
#	cursor.execute(query)
#	data = cursor.fetchall()
#	if session.get('logged_in') is True:
#		return render_template('home.html', logged_in = True, username = session['username'])
#	return render_template('home.html')

#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')
	
#Define route for register
@app.route('/register')
def register():
	return render_template('register.html')
	
#Define route for upload
@app.route('/upload')
def upload():
	return render_template('upload.html', logged_in = True)

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password'].encode('utf-8')
	md5password = hashlib.md5(password).hexdigest()
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM users WHERE username = %s and password = %s'
	cursor.execute(query, (username, md5password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	if data:
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		session['logged_in'] = True
		return redirect(url_for('home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)
		
#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password'].encode('utf-8')
	md5password = hashlib.md5(password).hexdigest()
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM users WHERE username = %s'
	cursor.execute(query, username)
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if data:
		#If the previous query returns data, then user exists
		error = "This user already exists."
		return render_template('register.html', error=error)
	else:
		ins = 'INSERT INTO users VALUES(%s, %s)'
		cursor.execute(ins, (username, md5password))
		conn.commit()
		cursor.close()
		success = "Registration Sucessful! Log in below to get started!"
		return render_template('login.html', success = success)
		
@app.route('/logout')
def logout():
	session.pop('username')
	session.pop('logged_in')
	now = datetime.datetime.now()
	success = 'logged out!'
	return redirect(url_for('home'))

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
	
@app.route('/uploading', methods=['POST'])
def uploading():
	username = session['username']
	# Get the name of the uploaded file
	file = request.files['file']
	# Check if the file is one of the allowed types/extensions
	if file and allowed_file(file.filename):
		# Make the filename safe, remove unsupported chars
		filename = secure_filename(file.filename)
		# Move the file form the temporal folder to
		# the upload folder we setup
		now = datetime.datetime.now()
#		currtime = "%s-%s-%s %s:%s:%s" % (str(now.year), str(now.month), str(now.day), str(now.hour), str(now.minute), str(now.second))
		cursor = conn.cursor()
		path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		file.save(path)
		caption = request.form['caption']
		ins = 'INSERT INTO pictures VALUES(%s, %s, CURRENT_TIMESTAMP, %s)'
		cursor.execute(ins, (username, path, caption))
		conn.commit()
		cursor.close()
		fullpath = "./" + path
		print fullpath
		# Redirect the user to the uploaded_file route, which
		# will basicaly show on the browser the uploaded file
		return render_template('upload.html', success = True, filepath = fullpath)

app.secret_key = 'secret key 123 best key ever'
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)