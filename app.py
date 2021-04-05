# -*- coding: utf-8 -*-
import os, random
import flask
from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from twilio.rest import Client
import serial
from serial import Serial

app = Flask(__name__)

def send_sms(msg, to):
    sid = "AC47750f02f5cb9b7e499915e9bb31fcbe"
    auth_token = "35a4d6a7ef3e86c2553d8a5e62e51161"
    twilio_number = "+16309341231"
    client = Client(sid, auth_token)
    message = client.messages.create(body=msg, from_=twilio_number, to=to)


#database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(3), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    blood = db.Column(db.String(10), nullable=False)
    pulse = db.Column(db.Integer)

    def __repr__(self):
        return f"<users {self.id}>"


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', data = Users.query.all())

@app.route('/users', methods=['GET', 'POST'])
def add_user():
    try:
        p = Users(name=request.form['name'], gender=request.form['gender'], age=request.form['age'], blood=request.form['blood'])
        db.session.add(p)
        db.session.commit()
    except:
        db.session.rollback()
        print('Ошибка добавления')
    return render_template('users.html', users=Users.query.all())

@app.route('/del_user', methods=['GET', 'POST'])
def del_user():
    var = int(request.form['id'])
    try:
        p = Users.query.filter_by(id=var).first()
        db.session.delete(p)
        db.session.commit()
    except:
        db.session.rollback()
        print('Ошибка удаления')
    return render_template('del_user.html', users=Users.query.all())

@app.route('/people', methods=['GET', 'POST'])
def people():
    var = int(request.args.get('my_var', None))
    p = Users.query.filter_by(id=var).first()

    pulse = 0
    ser = Serial('COM2', baudrate = 9600)
    data = ser.read()
    data = data.decode('utf-8')
    try:
        data = int(data)
        pulse = 10*pulse + data
    except:
        data = 0
    data = ser.read()
    data = data.decode('utf-8')
    try:
        data = int(data)
        pulse = 10*pulse + data
    except:
        data = 0
    data = ser.read()
    data = data.decode('utf-8')
    try:
        data = int(data)
        pulse = 10*pulse + data
    except:
        data = 0

    p.pulse = pulse
    db.session.commit()
    return render_template('people.html', data=p)

@app.route('/sms', methods=['GET', 'POST'])
def sms():
    name = request.form['name']
    pulse = request.form['pulse']
    to = request.form['phone']
    lat = request.form['lat']
    long = request.form['long']
    msg = name+' - состояние критическое, пульс '+pulse+', координаты {}, {}'.format(lat, long)
    #send_sms(msg, to)
    return render_template('sms.html', data=(msg, to))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
