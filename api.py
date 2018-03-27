from gevent import monkey

monkey.patch_all()

import os
from setproctitle import setproctitle

import flask
from flask import Flask
from flask_cors import CORS
from jinja2 import Environment, PackageLoader, select_autoescape

STATIC_EXTENSIONS = {'.jpg', '.ico', '.png', '.map', '.js', '.svg', '.json', '.css'}


class App:
    def __init__(self, production=True, real_time=False):
        self.app = app = Flask(__name__,
                               # static_url_path="",
                               static_folder='build',
                               template_folder='build')
        app.config['SECRET_KEY'] = 'secret!'
        CORS(app)

        app.debug = not production

        @app.route("/404/")
        def not_found():
            jinja_env = Environment(
                loader=PackageLoader('templates'),
                autoescape=select_autoescape(['html', 'xml'])
            )

            template = jinja_env.get_template('404.html')
            return template.render(), 404

        @app.route("/", defaults={"url": ""})
        @app.route('/<path:url>')
        def catch_all(url):
            """ Handle the page-not-found - apply some backward-compatibility redirect """
            if url == "" and production is False:
                return flask.redirect("http://localhost:3000")  # go to the webpack server

            ext = os.path.splitext(url)[-1]
            if ext in STATIC_EXTENSIONS:
                return flask.send_from_directory('ui/build', url)
            return flask.render_template("index.html")  # this comes from /build

        self.real_time = real_time
        if real_time:
            from flask_socketio import SocketIO

            self.socketio = socketio = SocketIO(app,
                                                logger=False,
                                                message_queue='redis://',
                                                channel='dashapi',
                                                async_mode='gevent',
                                                )

            socketio.server.on('data', lambda msg: print("gotmsg", msg))

            @socketio.on('data')
            def on_data(data):
                print('Data received', data)

            @socketio.on('connect')
            def on_connect():
                agent = flask.request.headers.get('user_agent')
                print(f'Client connected: {agent}')

            @socketio.on('disconnect')
            def on_disconnect():
                print('Client disconnected')
        else:
            self.socketio = None

    def run(self, host='127.0.0.1', port=3001):
        if self.real_time:
            setproctitle('api webserver [Dashboard]')
            self.socketio.run(self.app, host=host, port=port)
        else:
            setproctitle('api webserver [RT-Dashboard]')
            self.app.run(host=host, port=port)


if __name__ == '__main__':
    def main():
        app = App(production=True, real_time=True)

        app.run(host='127.0.0.1', port=3001)


    main()
