from flask import Flask,render_template,request,flash,redirect,url_for,logging,session,sessions
from flask_mysqldb import MySQL,MySQLdb
from wtforms import Form, StringField, TextAreaField, validators
from werkzeug.utils import secure_filename
import MySQLdb
from mysql.connector import MySQLConnection, Error
from functools import wraps
#from tables import Results
app = Flask(__name__)

#configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'emkay2020'
app.config['MYSQL_DB'] = 'metro'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['MYSQL_PORT'] = 3307
#initialize sql
mysql = MySQL(app)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/About')
def About():
    return render_template('About.html')

@app.route('/application', methods=['GET','POST'])
def application():
    if request.method =='POST':
        flash("REGISTRATION SUCCESSFUL")
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        position = request.form['position']
        email = request.form['email']
        phoneNumber = request.form['phoneNumber']
        dateofbirth = request.form['birth']
        education = request.form['education']
        means = request.form['means']
        maritalStatus = request.form['marital']
        trainings= request.form['trainings']
        residence = request.form['residence']
        experince = request.form['experience']
        cv = request.files['file']
        cv.save(secure_filename(cv.filename))
        
        cur = mysql.connection.cursor()
        #execute query
        cur.execute("INSERT INTO applicants(FirstName, LastName, Position, Email, PhoneNumber,DateOfBirth, Education, Means, MaritalStatus, Trainings, Residence, Experience, CV) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)", (firstName, lastName, position, email, phoneNumber,dateofbirth, education, means, maritalStatus, trainings, residence, experince, cv))
        #commit to DB
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('application'))
    return render_template('application.html')
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        password_candidate = request.form['password']
        cur = mysql.connection.cursor()
        result = cur.execute('SELECT * FROM admin WHERE username=%s',[uname])
        if result >0:
            data = cur.fetchone()
            password = data['password']
            if password_candidate == password:
                session['logged_in'] = True
                session['username'] = uname
                flash('You are nom Logged in')
                return redirect(url_for('admin'))
    return render_template('login.html')

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            return redirect(url_for('login'))
    return wrap

@app.route('/admin')
@is_logged_in
def admin():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM applicants")
    data = cur.fetchall()
    cur.close()
    return render_template('admin.html', applicants=data )

@app.route('/delete/<string:id_data>', methods = ['GET'])
@is_logged_in
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM applicants WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('admin'))

@app.route('/update',methods=['POST','GET'])
@is_logged_in
def update():

    if request.method == 'POST':
        id = request.form['id']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        position = request.form['position']
        email = request.form['email']
        phoneNumber = request.form['phoneNumber']
        dateofbirth = request.form['birth']
        education = request.form['education']
        means = request.form['means']
        maritalStatus = request.form['marital']
        trainings= request.form['trainings']
        residence = request.form['residence']
        experince = request.form['experience']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE applicants
               SET FirstName=%s, LastName=%s, Position=%s, Email=%s, PhoneNumber=%s,DateOfBirth=%s, Education=%s, Means=%s, MaritalStatus=%s, Trainings=%s, Residence=%s, Experience=%s
               WHERE id=%s
            """, (firstName, lastName, position ,email, phoneNumber,dateofbirth,education,means,maritalStatus,trainings,residence,experince,id))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('admin'))

@app.route('/insert', methods = ['POST'])
@is_logged_in
def insert():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        position = request.form['position']
        email = request.form['email']
        phoneNumber = request.form['phoneNumber']
        dateofbirth = request.form['birth']
        education = request.form['education']
        means = request.form['means']
        maritalStatus = request.form['marital']
        trainings= request.form['trainings']
        residence = request.form['residence']
        experince = request.form['experience']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO applicants(FirstName, LastName, Position, Email, PhoneNumber,DateOfBirth, Education, Means, MaritalStatus, Trainings, Residence, Experience) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)", (firstName, lastName, position, email, phoneNumber,dateofbirth, education, means, maritalStatus, trainings, residence, experince))
        mysql.connection.commit()
        return redirect(url_for('admin'))

app.secret_key = 'emkay2020'

if __name__ == '__main__':
    app.run(debug=True)