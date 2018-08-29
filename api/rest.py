import json
from flask import request, abort, jsonify
from flask_restful import Resource, reqparse
from bson.objectid import ObjectId
from api import mongo, api, app, utils
from werkzeug.datastructures import FileStorage
import uuid
import os


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    return '.' in filename and ext in ALLOWED_EXTENSIONS, ext

class Root(Resource):
    def get(self):
        return {
            'status': 'OK',
            # 'mongo': str(mongo.db),
        }

class Disease(Resource):
    def get(self, disease_id):
        return mongo.db.diseases.find_one_or_404({"_id": disease_id})


class LocationList(Resource):
    def __init__(self, *args, **kwargs):
            super(LocationList, self).__init__()
            
    def get(self):
        return  [x for x in mongo.db.location.find()]        
        
class DiseaseList(Resource):
    def __init__(self, *args, **kwargs):
            self.parser = reqparse.RequestParser()
            self.parser.add_argument('file', type=FileStorage, location='files', required=True, help="no file uploaded")
            self.parser.add_argument('location', type=str)
            super(DiseaseList, self).__init__()
            
    def get(self):
        return  [x for x in mongo.db.diseases.find()]

    def post(self):
        args = self.parser.parse_args()
        location = args['location']
        print(args)
        file = args['file']
        if not file:
            abort(400)
        allowed, ext = allowed_file(file.filename)
        if allowed:
            name = uuid.uuid4().hex
            filename = name + "." + ext
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            outp = utils.predict(filename)
            # print('outp', outp)
            output = json.loads(json.dumps(outp))
            # print('output: ', output)
            # print('status: ', output['status'])
            if output['status']:
                name = output['disease']['name']
                id = mongo.db.diseases.find_one({'name' : name})
                if not id:
                    mongo.db.diseases.insert(output['disease'])
                id = mongo.db.location.find_one({'location' : location, 'disease': name})
                if not id:
                    id = mongo.db.location.insert({'location': location, 'disease': name })
                return mongo.db.location.find_one({"_id": id})
            return jsonify({'result' : output})
        abort(400)
        
api.add_resource(Root, '/')
api.add_resource(LocationList, '/locations')
api.add_resource(DiseaseList, '/diseases')
api.add_resource(Disease, '/diseases/<ObjectId:disease_id>')
# api.add_resource(Disease, '/diseases/<ObjectId:name>')

