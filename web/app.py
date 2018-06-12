#!/usr/bin/env python
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dogs > cats'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


def check_date(d):
    try:
        m = re.search("^(0?[1-9]|[12][0-9]|3[01])[-](0?[1-9]|1[012])[-]\\d{4}$", d)
        return m.group()
    except Exception:
        return False


def bot_ask():
    if 'name' not in session:
        emit('server_response', {'question': 'What is your name?', 'speaker': 'Bot', 'field': 'name'})
    elif 'sex' not in session:
        emit('server_response', {'question': 'Are you male or female?', 'speaker': 'Bot', 'field': 'sex'})
    elif 'dob' not in session:
        emit('server_response', {'question': 'When were you born (dd-mm-yyyy)?', 'speaker': 'Bot', 'field': 'dob'})
    elif 'smoker' not in session:
        emit('server_response', {'question': 'Are you a smoker?', 'speaker': 'Bot', 'field': 'smoker'})
    else:
        emit('server_response', {'question': 'Thank you. Rress "Done" for results',
                                 'speaker': 'Bot', 'field': 'done'})


@socketio.on('get_result')
def bot_result(msg):
    if 'smoker' in session:
        emit('bot_result', {'ans': '{} was born in {} and is a {} {}.'.format(session['name'], session['dob'],
                                                                              session['sex'], session['smoker'])})


@socketio.on('client_event')
def client_msg(msg):
    emit('server_response', {'question': msg['ans'], 'speaker': 'You'})
    if msg['field'] == 'name' and msg['ans']:
        session['name'] = msg['ans']
    elif msg['field'] == 'sex' and msg['ans'].lower() in ['male', 'female']:
        session['sex'] = msg['ans']
    elif msg['field'] == 'dob' and check_date(msg['ans']):
        session['dob'] = check_date(msg['ans'])
    elif msg['field'] == 'smoker' and msg['ans'].lower() in ['yes', 'no', 'non-smoker']:
        session['smoker'] = 'smoker' if msg['ans'] == 'yes' else 'non-smoker'
    bot_ask()


@socketio.on('connect_event')
def connected_msg(msg):
    if msg['new_user']:
        emit('server_response', {'question': ('Hello, I am going to ask you a few questions'
                                              'that will help me know you better?'),
                                 'field': '', 'speaker': 'Bot'})
        bot_ask()
    else:
        emit('server_response', {'question': '... something is wrong', 'speaker': 'Bot'})


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)
