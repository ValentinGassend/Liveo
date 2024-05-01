import socketio

# Connect to the server
sio = socketio.Client()
sio.connect('http://192.168.1.16:3000/')

@sio.event
def connect():
    print('Connected to server')
    # sio.emit('message', 'banane')  # Emit the "message" event
    sio.emit('message', 'This is my data')  # Emit the "message" event
    print("data_sended")
    sio.disconnect()


sio.on('connect',connect())
