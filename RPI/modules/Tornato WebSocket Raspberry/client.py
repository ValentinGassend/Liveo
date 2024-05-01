import tornado.websocket
import asyncio
import logging
import RPi.GPIO as GPIO
from time import sleep


async def main():
    print('Starting main')
    
    conn = await tornado.websocket.websocket_connect('ws://192.168.1.16:8081/chatsocket')

    conn.write_message('device')
    # conn.write_message('controller')

    while True:

        message = await conn.read_message()
        try:
            value = int(message)
            logging.warn(value)
        except:
            logging.warn('"%s" is not integer. Ignore it', message)


if __name__ == "__main__":
    logging.warn('Starting program')

    try:
        ioloop = asyncio.get_event_loop()
        ioloop.run_until_complete(main())
        ioloop.close()
    except KeyboardInterrupt:
        pass