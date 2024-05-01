import tornado.websocket
import asyncio
import logging
import RPi.GPIO as GPIO
from time import sleep


# async def main():
    
#     conn = await tornado.websocket.websocket_connect('ws://192.168.1.16:8081/chatsocket')

#     conn.write_message('device')
#     # conn.write_message('controller')

#     while True:

#         message = await conn.read_message()
#         try:
#             value = int(message)
#             logging.warn(value)
#         except:
#             logging.warn('"%s" is not integer. Ignore it', message)


class TornadoWebsocketClient:
    def __init__(self, port=8081):
        self.conn = False
        self.port = port 
        self.prev_message=""
        # self.conn = await tornado.websocket.websocket_connect('ws://192.168.1.16:'+str(port)+'/chatsocket')
        # self.conn.write_message('RPI')
    def connect(self):
        try:
            self.ioloop = asyncio.get_event_loop()
            self.ioloop.run_until_complete(self._TryConnection())
            # self.ioloop.close()
        except KeyboardInterrupt:
            
            self.ioloop.close()
            pass

    async def _TryConnection(self):
        self.conn = await tornado.websocket.websocket_connect('ws://192.168.1.16:'+str(self.port)+'/chatsocket')
        self.send('RPI')

    def run (self):
        message = self.conn.read_message()
        if not str(message) == self.prev_message :
            print("Message recieved : " + str(message))
        self.prev_message = str(message)

    def send(self, data):
        self.conn.write_message(data)

# if __name__ == "__main__":
#     logging.warn('Starting program')

#     try:
#         ioloop = asyncio.get_event_loop()
#         ioloop.run_until_complete(main())
#         ioloop.close()
#     except KeyboardInterrupt:
#         pass


# myClient = TornadoWebsocketClient()
# myClient.connect()
# # try:
# #     ioloop = asyncio.get_event_loop()
# #     ioloop.run_until_complete(main())
# #     ioloop.close()
# # except KeyboardInterrupt:
# #     pass
# while True:
#     myClient.run()
