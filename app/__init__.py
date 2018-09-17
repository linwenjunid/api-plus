from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
conf = Config()


def create_app():
    app = Flask(__name__)
    app.config.from_object(conf)

    # @app.after_request
    # def after_request(response):
    #     response.headers.add('Access-Control-Allow-Origin', '*')
    #     if request.method == 'OPTIONS':
    #         response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
    #         headers = request.headers.get('Access-Control-Request-Headers')
    #         if headers:
    #             response.headers['Access-Control-Allow-Headers'] = headers
    #     return response

    conf.init_app(app)
    db.init_app(app)

    from .plus import plus as plus_blueprint
    app.register_blueprint(plus_blueprint, url_prefix='/plus')

    return app
