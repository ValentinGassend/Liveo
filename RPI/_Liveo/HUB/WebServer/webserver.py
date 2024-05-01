from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, emit
import multiprocessing


class WebServer:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, async_mode='eventlet')
        self.message_data = ""

        self.app.route('/')(self.index)
        self.app.route('/')(self.serve_font)
        self.socketio.on_event('connect', self.handle_connect)
        self.socketio.on_event('disconnect', self.handle_disconnect)
        self.socketio.on_event('message', self.handle_message)

    def serve_font(self, filename):
        return url_for('static', filename='images/logo_time.svg')

    def index(self):
        logo_time = url_for('static', filename='images/logo_time.svg')
        logo_date = url_for('static', filename='images/logo_date.svg')
        liveo = url_for('static', filename='images/liveo.svg')
        wave = url_for('static', filename='images/wave.svg')
        return render_template('test.html', message=self.message_data, logo_time=logo_time, logo_date=logo_date, liveo=liveo, wave=wave)

    def handle_connect(self):
        print('Client connected')

    def handle_disconnect(self):
        print('Client disconnected')

    def handle_message(self, message):
        self.message_data = message
        # print(message)
        emit('update', self.message_data, broadcast=True)

    def start(self):
        self.socketio.run(self.app, host=self.address,
                          port=self.port, log_output=False)

    def send_message(self, message):
        self.socketio.emit('update', message, broadcast=True)
