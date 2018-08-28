import datetime
import json
import time
from flask import Flask, request, jsonify
import os
import uuid
import prediction
import api

# from darpun_api import app
# from __init__ import app

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    return '.' in filename and ext in ALLOWED_EXTENSIONS, ext


@api.app.route("/", methods=["GET"])
def helloWorld():
    return "working..."
 
@api.app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    allowed, ext = allowed_file(file.filename)
    if file and allowed:
        name = uuid.uuid4().hex
        # print("file name: {} {}".format(name, ext))
        filename = name + "." + ext
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        output = api.prediction.predict(filename)
        return jsonify({'result' : output})
    return ''
 
if __name__ == "__main__":
    """
    this is run when the script is started.
    """
    api.app.run()
