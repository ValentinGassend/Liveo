import tornado.websocket
import tornado.web
import tornado.ioloop
import logging
import os.path
from tornado.options import define, options




class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/chatsocket", ChatSocketHandler),
        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "views"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            debug=options.debug,
        )
        super(Application, self).__init__(handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    ESP = None
    RPI = None

    def isDeviceOnline(self, device):
        return 'online' if device is not None else 'offline'
    
    def sendMessage(self, client, message):
        try:
            client.write_message(message)
        except:
            logging.error("Error sending message", exc_info=True)
    
    def open(self):
        logging.info('Client connected')

    def on_message(self, message):
        logging.info('Message received: %s', message)

        if 'RPI' == message:
            ChatSocketHandler.RPI = self
        elif 'ESP' == message:
            ChatSocketHandler.ESP = self

        if self == ChatSocketHandler.ESP:
            self.sendMessage(ChatSocketHandler.ESP, self.isDeviceOnline(self))
            if ChatSocketHandler.RPI is not None:
                logging.info('RPI is missing')
            else:
                self.sendMessage(ChatSocketHandler.RPI, self.isDeviceOnline(ChatSocketHandler.RPI))
        elif self == ChatSocketHandler.RPI:
            self.sendMessage(ChatSocketHandler.RPI, self.isDeviceOnline(self))
            if ChatSocketHandler.ESP is None:
                logging.info('ESP is missing')
            else:
                self.sendMessage(ChatSocketHandler.ESP, self.isDeviceOnline(ChatSocketHandler.ESP))
        else:
            logging.warn('Urgent! Somebody broke our super security connection!!!')

    def data_received(self, chunk):
        logging.info("data_received")

    def on_close(self):
        if ChatSocketHandler.ESP == self:
            logging.info('ESP leave')
            ChatSocketHandler.ESP = None
            if ChatSocketHandler.RPI is not None:
                self.sendMessage(ChatSocketHandler.RPI, self.isDeviceOnline())
        elif ChatSocketHandler.RPI == self:
            logging.info('RPI leave')
            ChatSocketHandler.RPI = None
            if ChatSocketHandler.ESP is not None:
                self.sendMessage(ChatSocketHandler.ESP, self.isDeviceOnline())


# def isDeviceOnline(device):
#     return 'online' if ChatSocketHandler.device is not None else 'offline'


# def sendMessage(client, message):
#     try:
#         client.write_message(message)
#     except:
#         logging.error("Error sending message", exc_info=True)


# def main():
#     tornado.options.parse_command_line()
#     app = Application()
#     app.listen(options.port)
#     tornado.ioloop.IOLoop.current().start()


# if __name__ == "__main__":
#     main()


class TornadoWebsocketServer:
    def __init__(self, port=8081):
        define("port", default=port, help="run on the given port", type=int)
        define("debug", default=True, help="run in debug mode")
        tornado.options.parse_command_line()
        app = Application()
        app.listen(options.port)
        tornado.ioloop.IOLoop.current().start()
    
    def isDeviceOnline():
        return 'online' if ChatSocketHandler.device is not None else 'offline'


    def sendMessage(client, message):
        try:
            client.write_message(message)
        except:
            logging.error("Error sending message", exc_info=True)

    def data_received(self, chunk):
        logging.info("data_received")

    def on_close(self):
        if ChatSocketHandler.ESP == self:
            logging.info('ESP leave')
            ChatSocketHandler.ESP = None
        elif ChatSocketHandler.RPI == self:
            logging.info('RPI leave')
            ChatSocketHandler.RPI = None
            if ChatSocketHandler.ESP is not None:
                self.sendMessage(ChatSocketHandler.ESP, self.isDeviceOnline())



MyTornadoWebsocket = TornadoWebsocketServer()