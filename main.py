from flask import Flask, render_template, request,redirect, session
import mysql.connector
import os


app = Flask(__name__)
app.secret_key=os.urandom(24)

conn = mysql.connector.connect(host="remotemysql.com", user="vkZoyiK0jG", password="xYGM5A65bc",
                               database="vkZoyiK0jG")
cursor=conn.cursor()

@app.route('/')
def login():
    return render_template('login.html')


@app.route('/forget')
def forget():
    return render_template('forget.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/')
@app.route('/login_validation' , methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')

    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email,password))
    users=cursor.fetchall()
    if len(users)>0:
        session['user_id']=users[0][0]
        return render_template('home.html')
    else:
        return render_template('login.html',info='Invalid Username or Password!')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')



if  __name__ == "__main__":
    app.run(debug=True)
