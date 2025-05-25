from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_migrate import Migrate
from clients.mqtt_client import MQTTClientWrapper

db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO()
swagger = Swagger()
mqtt_client = MQTTClientWrapper()