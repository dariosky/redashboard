from random import randint

import gevent
from flask_socketio import SocketIO

socketio = SocketIO(message_queue='redis://',
                    channel='dashapi',
                    async_mode='gevent', )

producer_id = randint(1, 100)


def send_random_data():
    data = {'title': f'Hello world {producer_id}-{randint(1, 100)}'}
    print(data)
    socketio.emit('data', data)


while True:
    try:
        send_random_data()
        gevent.sleep(1)
    except KeyboardInterrupt:
        break

print("The end")
