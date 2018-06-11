#!/usr/bin/env python
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit

app = Flask(__name__, template_folder='./')
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('client_event')
def client_msg(msg):
    emit('server_response', {'question': msg['ans'], 'speaker': 'You'})
    if msg['field'] == 'name':
        emit('server_response', {'question': 'Are you male or female?', 'speaker': 'Bot', 'field': 'sex'}) 
    elif msg['field'] == 'sex':
        emit('server_response', {'question': 'When were you born?', 'speaker': 'Bot', 'field': 'dob'}) 
    elif msg['field'] == 'dob':
        emit('server_response', {'question': 'Are you a smoker?', 'speaker': 'Bot', 'field': 'smoker'}) 
    elif msg['field'] == 'smoker':
        emit('server_response', {'question': 'Thank you. Rress "Done" for results', 'speaker': 'Bot', 'field': 'done'}) 

@socketio.on('connect_event')
def connected_msg(msg):
    #emit('server_response', {'data': msg['data']})
    if msg['new_user']:
        emit('server_response', {'question': 'Hello, I am going to ask you a few questions that will help me know you better?',
                                 'field': '', 'speaker': 'Bot'})
        emit('server_response', {'question': 'What is your name?', 'speaker': 'Bot', 'field': 'name'})
    else:
        emit('server_response', {'question': '... something is wrong', 'speaker': 'Bot'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)