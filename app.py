import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", 'sqlite:////tmp/test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

if app.env == "development":
    from flask_cors import CORS
    CORS(app)


@app.cli.command()
def update_data():
    from updater import Updater
    Updater().update_all()


from views import *

if __name__ == '__main__':
    app.run()
