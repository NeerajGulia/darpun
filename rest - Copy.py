import datetime
import json
import time
from flask import Flask, request, jsonify
import os
import uuid
import prediction
# from darpun_api import app
# from __init__ import app

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
MONGO_URL = os.environ.get('MONGO_URL')
if not MONGO_URL:
    MONGO_URL = "mongodb://localhost:27017/rest";
app.config['MONGO_URI'] = MONGO_URL
mongo = PyMongo(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 #1MB

def allowed_file(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    return '.' in filename and ext in ALLOWED_EXTENSIONS, ext


@app.route("/", methods=["GET"])
def helloWorld():
    return "working..."
 
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    allowed, ext = allowed_file(file.filename)
    if file and allowed:
        name = uuid.uuid4().hex
        # print("file name: {} {}".format(name, ext))
        filename = name + "." + ext
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        output = prediction.predict(filename)
        return jsonify({'result' : output})
    return ''
 
if __name__ == "__main__":
    """
    this is run when the script is started.
    """
    app.run()