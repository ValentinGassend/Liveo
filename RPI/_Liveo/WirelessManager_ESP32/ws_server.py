import os
import socket
import selectors
import time
from websocket import WebSocket


class ClientClosedError(Exception):
    pass


class WebSocketConnection:
    def __init__(self, addr, s, close_callback):
        self.client_close = False
        self._need_check = False

        self.address = addr
        self.socket = s
        self.ws = WebSocket(s, True)
        self.selector = selectors.DefaultSelector()
        self.close_callback = close_callback

        self.socket.setblocking(False)
        self.selector.register(self.socket, selectors.EVENT_READ)

    def read(self):
        events = self.selector.select(0)

        if not events:
            return

        # Check the flag for connection hung up
        if events[0][1] & selectors.EVENT_HUP:
            self.client_close = True

        msg_bytes = None
        try:
            msg_bytes = self.ws.read()
        except OSError:
            self.client_close = True

        # If no bytes => connection closed.
        if not msg_bytes or self.client_close:
            raise ClientClosedError()

        return msg_bytes

    def write(self, msg):
        try:
            self.ws.write(msg)
        except OSError:
            self.client_close = True

    def is_closed(self):
        return self.socket is None

    def close(self):
        print("Closing connection.")
        self.selector.unregister(self.socket)
        self.socket.close()
        self.socket = None
        self.ws = None
        if self.close_callback:
            self.close_callback(self)


class WebSocketClient:
    def __init__(self, conn):
        self.connection = conn

    def process(self):
        pass


class WebSocketServer:
    def __init__(self, page, connection_callback, disconnection_callback, max_connections=1):
        self._listen_s = None
        self._listen_selector = None
        self._clients = []
        self._max_connections = max_connections
        self._page = page
        self.disconnected = disconnection_callback
        self.connected = connection_callback
        self.is_connected = False

    def _setup_conn(self, port):
        self._listen_s = socket.socket()
        self._listen_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._listen_selector = selectors.DefaultSelector()

        addr = ("0.0.0.0", port)

        try:
            self._listen_s.bind(addr)
        except OSError as e:
            if e.errno == 98:
                print("Address already in use. Please choose a different port.")
                return
            else:
                raise

        self._listen_s.listen(1)
        self._listen_selector.register(self._listen_s, selectors.EVENT_READ)
        print("WebSocket started on ws://%s:%d" % (addr[0], port))

    def _check_new_connections(self, accept_handler):
        events = self._listen_selector.select(0)
        if not events:
            return

        if events[0][1] & selectors.EVENT_READ:
            accept_handler()

    def _accept_conn(self):
        cl, remote_addr = self._listen_s.accept()
        print("Client connection from:", remote_addr)
        self.connected()
        if len(self._clients) >= self._max_connections:
            # Maximum connections limit reached
            cl.setblocking(True)
            cl.sendall("HTTP/1.1 503 Too many connections\n\n".encode())
            cl.sendall("\n".encode())
            time.sleep(0.1)
            cl.close()
            return

        try:
            websocket_helper.server_handshake(cl)
        except OSError:
            # Not a websocket connection, serve webpage
            self._serve_page(cl)
            return

        self._clients.append(self._make_client(WebSocketConnection(remote_addr, cl, self.remove_connection)))

    def _make_client(self, conn):
        self.is_connected = True
        return WebSocketClient(conn)

    def _serve_page(self, sock):
        try:
            sock.sendall('HTTP/1.1 200 OK\nConnection: close\nServer: WebSocket Server\nContent-Type: text/html\n'.encode())
            length = os.stat(self._page)[6]
            sock.sendall('Content-Length: {}\n\n'.format(length).encode())
            with open(self._page, 'r') as f:
                for line in f:
                    sock.sendall(line.encode())
        except OSError:
            pass
        sock.close()

    def stop(self):
        if self._listen_selector:
            self._listen_selector.unregister(self._listen_s)
        self._listen_selector = None
        if self._listen_s:
            self._listen_s.close()
        self._listen_s = None

        for client in self._clients:
            client.connection.close()
        print("Stopped WebSocket server.")

    def start(self, port=8081):
        if self._listen_s:
            self.stop()
        self._setup_conn(port)
        print("Started WebSocket server.")

    def process_all(self):
        self._check_new_connections(self._accept_conn)

        for client in self._clients:
            client.process()

    def remove_connection(self, conn):
        for client in self._clients:
            if client.connection is conn:
                self._clients.remove(client)
                self.is_connected = False
                self.disconnected()
                return


class WSClient(WebSocketClient):
    def __init__(self, conn, received_callback):
        super().__init__(conn)
        self.received_callback = received_callback

    def process(self):
        try:
            msg = self.connection.read()
            if not msg:
                return
            msg = msg.decode("utf-8")
            self.received_callback(msg)
        except ClientClosedError:
            self.connection.close()

    def send_data(self, data_to_send):
        self.connection.write(data_to_send)

class WSServer(WebSocketServer):
    def __init__(self, connection_callback, disconnection_callback, received_callback):
        super().__init__("test.html", connection_callback, disconnection_callback, 2)
        self.is_connected = False
        self.received_callback = received_callback

    def _make_client(self, conn):
        self.cli = WSClient(conn, self.received_callback)
        self.is_connected = True
        return self.cli

    def send_data(self, data_to_send):
        self.cli.send_data(data_to_send)
