import os
from flask_restful import Api
from flask_pymongo import PyMongo
from flask import make_response, Flask
from bson.json_util import dumps
import logging
import logging.handlers
from flask_cors import CORS
from predict.model import Predict
from keras.models import load_model
import tensorflow as tf
import csv

application = Flask(__name__)
CORS(application)

application.config['UPLOAD_FOLDER'] = 'uploads/'
application.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 #1MB
application.debug = False

MONGO_URL = os.environ.get('MONGO_URL')
# print('mongo url: ', MONGO_URL)
if not MONGO_URL:
    MONGO_URL = "mongodb://localhost:27017/test"; # give local url

application.config['MONGO_URI'] = MONGO_URL

GEO_URL = os.environ.get('GEO_URL')
# print('GEO_URL: ', GEO_URL)
if not GEO_URL:
    GEO_URL = "https://maps.googleapis.com/maps/api/geocode/json?&latlng="

application.config['GEO_URL'] = GEO_URL

mongo = PyMongo(application)

def output_json(obj, code, headers=None):
    resp = make_response(dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp

api = Api(application)
api.representations = {'application/json': output_json}

# Logging section

logLevel = os.environ.get('LOG_LEVEL')
if not logLevel:
    logLevel = logging.ERROR

handler = logging.FileHandler(os.environ.get("LOGFILE", "darpun.log"))
formatter = logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s")
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logLevel)
logger.addHandler(handler)

modelPath = os.environ.get('MODEL_PATH')
if not modelPath:
    modelPath = 'predict/resnet.h5'

# model = Predict(modelPath, 'predict/label_names.csv')
model = load_model(modelPath)
graph = tf.get_default_graph()
label_names = {}
with open('predict/label_names.csv') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        label_names[int(line[1])] = line[0]


import api.rest
