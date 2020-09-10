import logging
import os

from flask import Flask
from flask_restful import Api
from logging.handlers import RotatingFileHandler

from settings import MAX_CONTENT_LENGTH


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

if not os.path.exists('logs'):
    os.mkdir('logs')

log_file_path = os.path.join(os.getcwd(), 'logs', 'fileapi.log')
file_handler = RotatingFileHandler(log_file_path, maxBytes=10240,
                                   backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('FileApi startup.')

from api.views import FileApi
api = Api(app)
api.add_resource(FileApi, '/')
