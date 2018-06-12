#!/usr/bin/env python
import pytest
from app import app, socketio


@pytest.fixture
def client(request):
    return app, socketio


def test_a(client):

    user = socketio.test_client(app)
    bot = socketio.test_client(app)
    user.get_received()
    bot.get_received()

    # user connect event, chat server ask for name
    user.emit('connect_event', {'new_user': True})
    received = user.get_received()
    assert received == [{'name': 'server_response',
                         'args': [{'question': ('Hello, I am going to ask you a few questionsthat'
                                                ' will help me know you better?'),
                                   'field': '', 'speaker': 'Bot'}], 'namespace': '/'},
                        {'name': 'server_response',
                         'args': [{'question': 'What is your name?', 'speaker': 'Bot', 'field': 'name'}],
                         'namespace': '/'}]

    # repeat question if name is illegal
    user.emit('client_event', {'field': 'name', 'ans': ''})
    received = user.get_received()
    assert received == [{'name': 'server_response',
                         'args': [{'question': '', 'speaker': 'You'}], 'namespace': '/'},
                        {'name': 'server_response',
                         'args': [{'question': 'What is your name?', 'speaker': 'Bot', 'field': 'name'}],
                         'namespace': '/'}]

    # ask for gender if name is legal
    user.emit('client_event', {'field': 'name', 'ans': 'user_name'})
    received = user.get_received()
    assert received == [{'name': 'server_response',
                         'args': [{'question': 'user_name', 'speaker': 'You'}], 'namespace': '/'},
                        {'name': 'server_response',
                         'args': [{'question': 'Are you male or female?', 'speaker': 'Bot', 'field': 'sex'}],
                         'namespace': '/'}]

    # repeat question if gender is illegal
    user.emit('client_event', {'field': 'sex', 'ans': 'boy'})
    received = user.get_received()
    assert received == [{'name': 'server_response',
                         'args': [{'question': 'boy', 'speaker': 'You'}], 'namespace': '/'},
                        {'name': 'server_response',
                         'args': [{'question': 'Are you male or female?', 'speaker': 'Bot', 'field': 'sex'}],
                         'namespace': '/'}]

    # ask for dob if gender is legal
    user.emit('client_event', {'field': 'sex', 'ans': 'male'})
    received = user.get_received()
    assert received == [{'name': 'server_response',
                         'args': [{'question': 'male', 'speaker': 'You'}], 'namespace': '/'},
                        {'name': 'server_response',
                         'args': [{'question': 'When were you born (dd-mm-yyyy)?', 'speaker': 'Bot', 'field': 'dob'}],
                         'namespace': '/'}]

    # repeat question if dob is illegal
    user.emit('client_event', {'field': 'dob', 'ans': '11112018'})
    received = user.get_received()
    assert received == [{'name': 'server_response',
                         'args': [{'question': '11112018', 'speaker': 'You'}], 'namespace': '/'},
                        {'name': 'server_response',
                         'args': [{'question': 'When were you born (dd-mm-yyyy)?', 'speaker': 'Bot', 'field': 'dob'}],
                         'namespace': '/'}]

    # ask if user is smoker if dob is legal
    user.emit('client_event', {'field': 'dob', 'ans': '11-11-2018'})
    received = user.get_received()
    assert received == [{'name': 'server_response',
                         'args': [{'question': '11-11-2018', 'speaker': 'You'}], 'namespace': '/'},
                        {'name': 'server_response',
                         'args': [{'question': 'Are you a smoker?', 'speaker': 'Bot', 'field': 'smoker'}],
                         'namespace': '/'}]

    # repeat question if answer is illegal
    user.emit('client_event', {'field': 'dob', 'ans': 'nope'})
    received = user.get_received()
    assert received == [{'name': 'server_response',
                         'args': [{'question': 'nope', 'speaker': 'You'}], 'namespace': '/'},
                        {'name': 'server_response',
                         'args': [{'question': 'Are you a smoker?', 'speaker': 'Bot', 'field': 'smoker'}],
                         'namespace': '/'}]

    # thanks for all answers if answer is legal
    user.emit('client_event', {'field': 'smoker', 'ans': 'yes'})
    received = user.get_received()
    assert received == [{'name': 'server_response',
                         'args': [{'question': 'yes', 'speaker': 'You'}], 'namespace': '/'},
                        {'name': 'server_response',
                         'args': [{'question': 'Thank you. Rress "Done" for results', 'speaker': 'Bot', 'field': 'done'}],
                         'namespace': '/'}]

    # send result when your click done
    user.emit('get_result', {'ans': None})
    received = user.get_received()
    assert received == [{'name': 'bot_result',
                         'args': [{'ans': 'user_name was born in 11-11-2018 and is a male smoker.'}],
                         'namespace': '/'}]
