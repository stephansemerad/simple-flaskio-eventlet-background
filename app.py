#!/usr/bin/env python

import eventlet
eventlet.monkey_patch() # make sure to use eventlet and call eventlet.monkey_patch()
from flask import Flask, render_template, request, g, session, make_response, current_app, redirect, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
socketio = SocketIO(app, async_mode='eventlet')

switch = False
def do_work():
    global switch
    unit_of_work = 0
    while switch:
        unit_of_work += 1
        print(unit_of_work)
        socketio.emit("update", {"msg": unit_of_work},  broadcast =True)
        eventlet.sleep(1)


@app.route('/')
def index():
    return render_template('demo.html')

@socketio.on('connect')
def connect():
    ip = request.remote_addr
    print('connect')
    socketio.emit("update", {"msg": "connected from "+ ip}, broadcast =False)

@socketio.on('start')
def start_work():
    global switch
    switch = True
    print('start')
    socketio.emit("update", {"msg": "starting worker"},  broadcast =True  )
    socketio.start_background_task(target=do_work)


@socketio.on('stop')
def stop_work():
    global switch
    switch = False
    socketio.emit("update", {"msg": "worker has been stoppped"},  broadcast =True)


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=80, debug=True)
