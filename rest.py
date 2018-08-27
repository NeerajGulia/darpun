import datetime
import json
import time
from flask import Flask, request
# from darpun_api import app
# from __init__ import app

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 #1MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET"])
def helloWorld():
    return "working..."
 
@app.route('/upload', methods=['POST'])
def upload_file():
    if file and allowed_file(file.filename):
        filename = time.time()
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "file successfully saved"
    return ''
 
if __name__ == "__main__":
    """
    this is run when the script is started.
    """
    app.run()
