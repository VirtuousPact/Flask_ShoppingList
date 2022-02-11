from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():

        from .home import home_routes
        from .list import list_routes

        #TODO: add blueprints
        app.register_blueprint(home_routes.home_bp)
        app.register_blueprint(list_routes.list_bp)

        return app
