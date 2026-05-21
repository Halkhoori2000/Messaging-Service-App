import os

from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Channel data
active_users = dict()   # username -> channel
channels = dict()       # channel -> [messages]

# Main page route
@app.route("/")
def index():
    return render_template('index.html') 

# Socket IO handlers
@socketio.on('login')
def on_login(data):
    username = data['username']

    if username not in active_users:
        active_users[username] = None
    
    channel = active_users[username]
    emit('login', {'username': username, 'channel': channel, 'channels': list(channels.keys())})


@socketio.on('join')
def on_join(data):
    channel = data['channel']
    username = data['username']

    # Check if channel is present 
    if channel not in channels:
        return 
    
    # Check if user is active
    if username not in active_users:
        return 
    
    # Leave previous channel
    if active_users[username] is not None:
        leave_room(active_users[username])

    # Join the room
    join_room(channel)

    # Set the user's channel
    active_users[username] = channel

    # Emit the event 
    emit('join', {'channel': channel, 'messages': channels[channel]})


@socketio.on('open')
def on_open(data):
    channel = data['channel']

    # Check if channel is already opened
    if channel in channels:
        return 
    
    # Create a new channel 
    channels[channel] = [] 

    # Inform all users 
    emit('open', {'channel': channel}, broadcast=True)

@socketio.on('send')
def on_send(data):
    username = data['username']

    # Validate user
    if username not in active_users:
        return 
    
    channel = active_users[username]
    
    # Validate channel
    if channel not in channels:
        return 
    
    # Add timestamp 
    data['timestamp'] = datetime.now().isoformat()
    
    # Send the message
    channel = active_users[username]
    channels[channel].append(data)

    # Limit saved messages to 100
    channels[channel] = channels[channel][-100:]    

    # Emit to the room
    emit('send', data, to=channel)

@socketio.on('logout')
def on_logout(data):
    username = data['username']

    # Validate user 
    if username in active_users:
        # Leave room
        channel = active_users[username]

        if channel is not None:
            leave_room(channel)

        # Remove from active users
        del active_users[username]

    # Send message
    emit('logout')

@socketio.on('leave')
def on_leave(data):
    username = data['username']

    # Validate user
    if username in active_users:
        channel = active_users[username]

        if channel in channels:
            # Clear the channel
            leave_room(channel)
            active_users[username] = None

    emit('leave')

@socketio.on('delete')
def on_delete(data):
    # Validate channel
    channel = data['channel']

    if channel in channels:
        # Find the message
        for i in range(len(channels[channel])):
            msg = channels[channel][i]

            # Check if we found the message
            if msg['username'] == data['username'] and msg['message'] == data['message'] and msg['timestamp'] == data['timestamp']:
                del channels[channel][i]
                break 
        
        # Inform users of the deleted message
        emit('delete', data, to=channel)
# Start the socket 
if __name__ == '__main__':
    socketio.run(app, debug=True)