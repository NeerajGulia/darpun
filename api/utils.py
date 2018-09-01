from api import *
import json
import requests
from api.schema import Prediction, Disease, Remedy, Location, Geocode, ComplexHandler
import logging
import os
import numpy as np
import asyncio

log = logging.getLogger(__name__) 

def getJson(obj):
    return json.loads(json.dumps(obj, default=ComplexHandler))

def predict(filepath):
    output = model.make_prediction(filepath)
    print('predict output: ' + str(output))
    # print('predict: filepath: {}, prediction: {}'.format(filepath, output))
    if len(output) > 0:
        diseaseName = output[0][0]
        conf = output[0][1]
        remedy = None
        disease = getDisease(diseaseName)
        if disease:
            remedy = getRemedy(disease.remedyName)
        if disease is not None:
            p = Prediction()
            p.status = True
            p.disease = disease
            p.remedy = remedy
            p.confidence = str(conf) + "%"
            return getJson(p)

    predict = Prediction()
    predict.status = False
    predict.message = 'We are not able to predict the disease for given image'
    return getJson(predict)
    
def getDisease(name):
    d = mongo.db.diseases.find_one({'name' : name})
    if not d:
        return None
    output = Disease()
    output.name = name
    output.description = d.get('description', '')
    output.remedyName = d.get('remedyName', '')
    return output

def getRemedy(name):
    r = mongo.db.remedies.find_one({'name' : name})
    if not r:
        return None
    output = Remedy()
    output.name = name
    output.description = r.get('description', '')
    output.medicine = r.get('medicine', '')
    output.dose = r.get('dose', '')
    output.remarks = r.get('remarks', '')
    return output


def fireAndForget(task, *args, **kwargs):
    loop = asyncio.new_event_loop()
    if callable(task):
        return loop.run_in_executor(None, task, *args, **kwargs)
    else:    
        print('Task must be a callable')
    
def tryAddLocation(lat, lng, disease):
    try:
        # print('tryAddLocation: lat: {}, lng: {}, disease: {}'.format(lat, lng, disease))
        # location = mongo.db.location.find_one({'geocode' : {'lat' : lat, 'lng': lng}, 'disease': disease})
        if mongo.db.location.find_one({'geocode' : {'lat' : lat, 'lng': lng}, 'disease': disease}):
            return #we already have data for this geocode and disease, so not adding it again
        geocode = Geocode()
        geocode.lat = lat
        geocode.lng = lng
        loc = Location()
        loc.geocode = geocode
        loc.disease = disease
        output = getGeoInfo(lat, lng)
        # print('tryAddLocation: output: ', output)
        if output is not None:
            loc.pincode = output.get('postal_code', None)
            loc.city = output.get('administrative_area_level_2', None)
            loc.state = output.get('administrative_area_level_1', None)
            loc.country = output.get('country', None)
            if loc.pincode is None or loc.city is None or loc.state == None or loc.country == None:
                log.warning("tryAddLocation: Something is not right: {}".format(json.dumps(loc, default=ComplexHandler)))
                return
            dumpedLoc = getJson(loc)
            mongo.db.location.insert(dumpedLoc)
    except Exception as e :
        msg = 'tryAddLocation exception: {}'.format(str(e))
        print(msg)
        log.error(msg)

def getGeoInfo(lat, lng):
    url = (application.config['GEO_URL'] + lat + "," + lng)
    result = requests.get(url)
    js = result.json()
    if result.status_code != 200 or len(js['results']) == 0:
        return None
    names = {}
    for i in range(len(js['results'][0]['address_components'])):
        names[js['results'][0]['address_components'][i]['types'][0]] = js['results'][0]['address_components'][i]['long_name']
    return names
            