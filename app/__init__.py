from flask import Flask
    from .config import DevelopmentConfig
    from .db import db
    from .extensions import init_extensions
    from .routes.tasks import bp as tasks_bp
    from .routes.users import bp as users_bp
    from flask_migrate import Migrate


def create_app(config_class=None):
    app = Flask(__name__)
    app.config.from_object(config_class or DevelopmentConfig)

    db.init_app(app)
    Migrate(app, db)

    init_extensions(app, db)

    app.register_blueprint(tasks_bp)
    app.register_blueprint(users_bp)

    @app.route('/')
    def index():
        return {'status': 'ok'}, 200

    return app

# for manage.py
app = create_app()