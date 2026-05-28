from flask import Flask, render_template, request
import mysql.connector
import re

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        mydb = mysql.connector.connect(
                    host="remotemysql.com",
                    user="wXy63pU5g1",
                    password="qVOgRNMGRK",
                    database="wXy63pU5g1"
        )

        mycursor = mydb.cursor()
        mycursor.execute('SELECT * FROM LoginDetails WHERE username = %s AND password = %s', (username, password))
        account = mycursor.fetchone()
        if account:
            print("Login success")
            name = account[1]
            id = account[0]
            msg = 'Logged in successfully!'
            print("Login Successfull!")
            return render_template('welcome.html', msg=msg, name=name, id=id)
        else:
            msg = 'Incorrect username/password!'
            return render_template('login.html', msg=msg)
    else:
        return render_template('login.html')
    
@app.route('/logout')
def logout():
    name = ''
    id = ''
    msg = 'You have been logged out!'
    return render_template('login.html', msg=msg,)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        mydb = mysql.connector.connect(
                    host="remotemysql.com",
                    user="wXy63pU5g1",
                    password="qVOgRNMGRK",
                    database="wXy63pU5g1"
        )

        mycursor = mydb.cursor()
        print(username)
        mycursor.execute('SELECT * FROM LoginDetails WHERE username = %s AND email = %s', (username, email))
        account = mycursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            mycursor.execute('INSERT INTO LoginDetails(username, password, email) VALUES (%s, %s, %s)',(username, password, email))
            mydb.commit()
            msg = 'You have successfully registered!'
            name = username
            return render_template('login.html', msg=msg, name=name)
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('login.html')

app.run(host='0.0.0.0', port=8080, debug=True)