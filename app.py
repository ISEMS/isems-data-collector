import os
from datetime import datetime, date
from json import JSONEncoder

from flask import Flask
from flask.json.provider import DefaultJSONProvider
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry
class CustomJSONProvider(DefaultJSONProvider):
    def default(self, o):
        if isinstance(o, date) or isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", 'sqlite:////tmp/test.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json = CustomJSONProvider(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
if os.environ.get("SENTRY_DSN"):
    sentry = Sentry(app)

if app.env == "development":
    from flask_cors import CORS
    CORS(app)


@app.cli.command()
def update_data():
    from updater import Updater
    Updater().update_all()


@app.cli.command()
def subscribe():
    from mqtt_client import MQTTClient
    MQTTClient().start()


from views import *

if __name__ == '__main__':
    app.run()
