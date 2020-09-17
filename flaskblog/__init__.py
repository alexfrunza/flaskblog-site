from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config
from flask_migrate import Migrate
from flask_discord import DiscordOAuth2Session


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
migrate = Migrate()
discord_oauth = DiscordOAuth2Session()


def create_app(config_class=Config):
    global discord_oauth

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    discord_oauth.init_app(app)

    from flaskblog.users.routes import users
    app.register_blueprint(users)

    from flaskblog.posts.routes import posts
    app.register_blueprint(posts)

    from flaskblog.main.routes import main
    app.register_blueprint(main)

    from flaskblog.errors.handlers import errors
    app.register_blueprint(errors)

    return app
