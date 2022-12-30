import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


def set_postgres_db_uri() -> str:
    """
    Returns the database uri to establish db connection
    """

    host = os.getenv("POSTGRES_DB_HOST")
    database = os.getenv("POSTGRES_DB")
    port = os.getenv("POSTGRES_DB_PORT")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")

    connection_string = (
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    )

    return connection_string


app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = set_postgres_db_uri()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)


from flaskr import routes
