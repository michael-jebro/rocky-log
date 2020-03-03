from flask import (Flask, request, make_response, session,
                   redirect, url_for, abort, render_template, send_file)

from flask_mail import Mail, Message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


import smtplib, ssl
from flask_sqlalchemy import SQLAlchemy
from sss_lib import SessionContainer
from passwrod import Passwrod
import email

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(20), unique=True, primary_key=True)
    email = db.Column(db.String(120), unique=False, nullable=False)
    role = db.Column(db.String(1), unique=False, nullable=False)
    password = db.Column(db.String(64), unique=False, nullable=False)
    salt = db.Column(db.String(30), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


def create_admin_if_necessary():
    admin_exists = User.query.get('admin')
    if not admin_exists:
        password = SessionContainer.Controller().get_random_data()
        print('Admin password: ' + password)

        salt = SessionContainer.Controller().get_random_data()
        passwrod = Passwrod(password, salt)

        admin = User(
            username='admin',
            email='',
            role='a',
            password=passwrod.get_hash(),
            salt=salt
        )

        db.session.add(admin)
        db.session.commit()


session_container = SessionContainer()
db.create_all()
create_admin_if_necessary()

mail = Mail(app)


@app.route('/', methods=['GET', 'POST'])
def root():

    cookies = request.cookies
    return ''


@app.route('/login', methods=['GET', 'POST'])
def login():
    cookies = request.cookies
    print(cookies)
    if 'session' in cookies.keys():
        cur_uid = cookies['session']

        if session_container.is_active(cur_uid):
            response = make_response(
                redirect(url_for('profile'))
            )
            return response

    if request.method == 'POST':
        user = User.query.get(request.form['username'])
        if user:
            passwrod = Passwrod(
                request.form['passwrod'],
                user.salt
            )
            print(user.password, passwrod.get_hash())

            if passwrod.the_same_as_(user.password):
                uid = session_container.add_session_returning_uid(
                    user.username
                )

                response = make_response(
                    redirect(url_for('profile'))
                )

                response.set_cookie('session', uid)
                return response

        response = make_response(
            render_template('/template/wrong_usern_passwd.html')
        )

        return response

    response = make_response(
        render_template('login.html')
    )

    return response

@app.route('/register', methods=['GET', 'POST'])
def register():
    cookies = request.cookies
    print(cookies)
    if 'session' in cookies.keys():
        cur_uid = cookies['session']
        if session_container.is_active(cur_uid):
            response = make_response(
                redirect(url_for('profile'))
            )
            return response
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        salt = SessionContainer.controller().get_random_data()
        
        passwrod = Passwrod(
            request.form['passwrod'],
            salt
        )
        
        user = User(
            username=username,
            email=email,
            role='d',
            password=passwrod.get_hash()
        )
        #check if user exists in db and verify email
        db.session.add(user)
        db.session.commit()
        response = make_response(
            redirect(url_for('profile'))
        )
        return response

@app.route('/templates/<file_name>')
def get_html(file_name):
    return send_file('./templates/' + file_name)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    cookies = request.cookies
    print(cookies)
    if 'session' in cookies.keys():
        cur_uid = cookies['session']

        if session_container.is_active(cur_uid):
            return 'welcome'

    response = make_response(
        redirect(url_for('login'))
    )

    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
