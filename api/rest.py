import json
from flask import request, abort, jsonify
from flask_restful import Resource, reqparse
from bson.objectid import ObjectId
from api import utils, app, api, mongo, schema
from werkzeug.datastructures import FileStorage
import uuid
import os

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    return '.' in filename and ext in ALLOWED_EXTENSIONS, ext

class Disease(Resource):
    def get(self, disease_id):
        return mongo.db.diseases.find_one_or_404({"_id": disease_id})


class LocationList(Resource):
    def __init__(self, *args, **kwargs):
            super(LocationList, self).__init__()
            
    def get(self):
        return  [x for x in mongo.db.location.find({}, {'_id': False})]

class RemedyList(Resource):
    def __init__(self, *args, **kwargs):
            super(RemedyList, self).__init__()
            
    def get(self):
        return  [x for x in mongo.db.remedies.find({}, {'_id': False})]

        
class DiseaseList(Resource):
    def __init__(self, *args, **kwargs):
            self.parser = reqparse.RequestParser()
            self.parser.add_argument('file', type=FileStorage, location='files', required=True, help="no file uploaded")
            self.parser.add_argument('lat', type=str, help="Please provide geo latitude")
            self.parser.add_argument('lng', type=str, help="Please provide geo longitude")
            super(DiseaseList, self).__init__()
            
    def get(self):
        return  [x for x in mongo.db.diseases.find({}, {'_id': False})]

    def post(self):
        args = self.parser.parse_args()
        lat = args['lat']
        lng = args['lng']
        file = args['file']
        # print('file: {}, filename: {}'.format(file, file.filename))
        if not file or file.filename == '':
            abort(400)
        allowed, ext = allowed_file(file.filename)
        if allowed:
            name = uuid.uuid4().hex
            filename = name + "." + ext
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            outp = utils.predict(filepath)
            output = json.loads(outp)
            if output['status']:
                name = output['disease']['name']
                id = mongo.db.diseases.find_one({'name' : name})
                if not id: #we do not identify this desease yet
                    return jsonify({'result' : {'status': False, 'message': 'We are not able to predict the disease for given image'}})
                utils.tryAddLocation(lat, lng, name)
                return jsonify({'result' : output})
            return jsonify({'result' : {'status': False, 'message': output['message']}})
        abort(400)
        
api.add_resource(LocationList, '/api/locations')
api.add_resource(DiseaseList, '/api/diseases') 
api.add_resource(RemedyList, '/api/remedies')
api.add_resource(Disease, '/api/diseases/<ObjectId:disease_id>')

