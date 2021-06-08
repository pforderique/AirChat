from flask import session
from flask_socketio import send, emit, join_room, leave_room
from time import localtime, strftime
from . import socketio

@socketio.on('message')
def message(data):
    print(f"\n\n{data}\n\n")
    # sends that data to connected clients -- by default, it pushes it to the event bucket called 'message'
    send({
        'msg':data['msg'], 
        'username':data['username'], 
        'time_stamp': strftime('%b-%d %I:%M%p', localtime())
    }, room=data['room']) 
    # emit('some-event', 'this is a custom event message') # sends data to the 'some-event' bucket on clientside

@socketio.on('join')
def join(data):
    session['current_room'] = data['room']
    join_room(data['room'])
    send({'msg': data['username'] + ' has joined the room ' + data['room']}, room=data['room'] )

@socketio.on('leave')
def leave(data):
    leave_room(data['room'])
    send({'msg': data['username'] + ' has left the room ' + data['room']}, room=data['room'] )