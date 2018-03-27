from gevent import monkey

monkey.patch_all()

from functools import partial

import gevent
import socketio
from flask_socketio import SocketIO
from socketio import PubSubManager


class EavesDropManager(socketio.RedisManager):
    def _handle_emit(self, message):
        # Events with callbacks are very tricky to handle across hosts
        # Here in the receiving end we set up a local callback that preserves
        # the callback host and id from the sender
        remote_callback = message.get('callback')
        remote_host_id = message.get('host_id')
        if remote_callback is not None and len(remote_callback) == 3:
            callback = partial(self._return_callback, remote_host_id,
                               *remote_callback)
        else:
            callback = None
        for func in (self.callback, super(PubSubManager, self).emit):
            func(message['event'], message['data'],
                 namespace=message.get('namespace'),
                 room=message.get('room'),
                 skip_sid=message.get('skip_sid'),
                 callback=callback)

    def callback(self, event, data, namespace, room=None, skip_sid=None,
                 callback=None, **kwargs):
        print("Eavesdropped:", event, data)


client_manager = EavesDropManager(
    'redis://', channel='dashapi',
    write_only=False,  # subscribe to events
)

socketio = SocketIO(
    async_mode='gevent',
    server_options=dict(
        client_manager=client_manager
    )
)
socketio.init_app(app=None)
client_manager.set_server(socketio.server)
client_manager.initialize()


@socketio.server.on('data')
def on_data(message):
    print("Got message", message)


while True:
    try:
        gevent.sleep(1)
    except KeyboardInterrupt:
        break

print("The end")
