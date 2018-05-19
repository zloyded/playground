""" Mail reader and pase images linkg generate database and download images
"""
import os
from flask import Flask
from flask.ext.cors import CORS
from flask_environments import Environments
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
app.name = 'Mailer'
env = Environments(app)
config_file = os.path.join(os.path.abspath('./app'), 'config', 'config.yml')
secrets_file = os.path.join(os.path.abspath('./app'), 'config', 'secrets.yml') 
env.from_yaml(config_file)
env.from_yaml(secrets_file)
mongo = PyMongo(app)
CORS(app)
app.jinja_env.line_statement_prefix = '%'
from app import routers
