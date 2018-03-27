import os
from setproctitle import setproctitle

import flask
from flask import Flask
from flask_cors import CORS
from jinja2 import Environment, PackageLoader, select_autoescape

STATIC_EXTENSIONS = {'.jpg', '.ico', '.png', '.map', '.js', '.svg', '.json', '.css'}


def get_app(production=True):
    setproctitle('api webserver [RT-Dashboard]')
    app = Flask(__name__,
                # static_url_path="",
                static_folder='build',
                template_folder='build')
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

    return app


if __name__ == '__main__':
    app = get_app(production=False)
    host, port = '127.0.0.1', 3001
    app.run(host=host, port=port, threaded=True, debug=True, use_reloader=True)
