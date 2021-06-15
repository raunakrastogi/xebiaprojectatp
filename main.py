from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_mysqldb import MySQL, MySQLdb
# import mysql.connector
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config['MYSQL_HOST'] = "remotemysql.com"
app.config['MYSQL_USER'] = "vkZoyiK0jG"
app.config['MYSQL_PASSWORD'] = "xYGM5A65bc"
app.config['MYSQL_DB'] = "vkZoyiK0jG"
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# conn = mysql.connector.connect(host="remotemysql.com", user="vkZoyiK0jG", password="xYGM5A65bc",
#                       database="vkZoyiK0jG")
# cursor=conn.cursor()

mysql = MySQL(app)


@app.route('/')
def login():
    return render_template('login.html',)


@app.route('/forget/', methods=['GET', 'POST'])
def forget():
    if request.method == "POST":

        email = request.form['email']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
        users = cursor.fetchone()

        if users == None:
            flash("Account does not exist.")
            return redirect(url_for('forget'))
        else:
            return redirect(url_for('security', user=users['Name']))

    return render_template('forget.html')


@app.route('/security/<user>/', methods=['GET', 'POST'])
def security(user):
    if request.method == "POST":

        user = user.strip()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""SELECT * FROM `users` WHERE `name` LIKE '{}'""".format(user))
        users = cursor.fetchone()

        requested_dob = datetime.strptime(request.form['dob'], '%Y-%m-%d').date()

        if users['dob'] == requested_dob:
            session['user_pass_change'] = user
            return redirect(url_for('changepass'))
        else:
            flash("Incorrect Answer.")
            return redirect(url_for('security', user = users['Name']))

    return render_template('security_question.html', user=user)


@app.route('/changepass/', methods=['GET', 'POST'])
def changepass():
    if request.method == "POST":
        new_password = request.form['pass']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""UPDATE `users` SET `password` = '{}' WHERE `name` LIKE '{}'""".format(new_password, session[
            'user_pass_change']))
        mysql.connection.commit()

        session.pop('user_pass_change')

        flash('Password changed successfully :)', 'success')
        return redirect(url_for('login'))

    return render_template('change_password.html')


@app.route('/home')
def home():
    if 'user_id' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM employee ORDER BY id ASC")
        employee = cursor.fetchall()
        return render_template('home.html', employee=employee)
    else:
        return redirect('/')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email, password))
    users = cursor.fetchone()
    # users=cursor.fetchall()

    if users != None:
        # session['user_id']=users[0][0]
        session['user_id'] = users['Name']
        return redirect('/home')
    else:
        flash('Invalid Username/Password!','danger')
        return redirect('/')



@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
