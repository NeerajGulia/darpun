from api import *
import json
import requests
from api.schema import Prediction, Disease, Remedy, Location, Geocode, ComplexHandler
import logging

log = logging.getLogger(__name__) 

def predict(filename):

    diseaseName = 'Apple random name' # get this information from the model
    remedy = None
    disease = getDisease(diseaseName)
    if disease:
        remedy = getRemedy(disease.remedyName)
    if not disease or not remedy:
        predict = Prediction()
        predict.status = False
        predict.message = 'We are not able to predict the disease for given image'
        return json.dumps(predict, default=ComplexHandler)
    
    p = Prediction()
    p.status = True
    p.disease = disease
    p.remedy = remedy

    return json.dumps(p, default=ComplexHandler)

def getDisease(name):
    d = mongo.db.diseases.find_one({'name' : name})
    # print('getDisease: ', d)
    if not d:
        return None
    output = Disease()
    output.name = name
    output.description = d.get('description', '')
    output.remedyName = d.get('remedyName', '')
    return output

def getRemedy(name):
    r = mongo.db.remedies.find_one({'name' : name})
    # print('getRemedy: ', r)
    if not r:
        return None
    output = Remedy()
    output.name = name
    output.description = r.get('description', '')
    output.medicine = r.get('medicine', '')
    output.dose = r.get('dose', '')
    output.remarks = r.get('remarks', '')
    return output
    
def tryAddLocation(lat, lng, disease):
    try:
        # location = mongo.db.location.find_one({'geocode' : {'lat' : lat, 'lng': lng}, 'disease': disease})
        # print('tryAddLocation > location: ', location)
        if mongo.db.location.find_one({'geocode' : {'lat' : lat, 'lng': lng}, 'disease': disease}):
            return #we already have data for this geocode and disease, so not adding it again
        geocode = Geocode()
        geocode.lat = lat
        geocode.lng = lng
        loc = Location()
        loc.geocode = geocode
        loc.disease = disease
        output = getGeoInfo(lat, lng)
        if output != None:
            loc.pincode = output.get('postal_code', None)
            loc.city = output.get('administrative_area_level_2', None)
            loc.state = output.get('administrative_area_level_1', None)
            loc.country = output.get('country', None)
            if loc.pincode == None or loc.city == None or loc.state == None or loc.country == None:
                log.warning("tryAddLocation: Something is not right: {}".format(json.dumps(loc, default=ComplexHandler)))
                return
            dumpedLoc = json.dumps(loc, default=ComplexHandler)
            # print('tryAddLocation > dumpedLoc: ', dumpedLoc)
            dumpedLoc = json.loads(dumpedLoc)
            mongo.db.location.insert(dumpedLoc)
    except Exception as e :
        print('exception: {}'.format(str(e)))
        log.error('tryAddLocation: ', str(e))

def getGeoInfo(lat, lng):
    # print('getGeoInfo > lat: {}, lng: {}'.format(lat,lng))
    url = (app.config['GEO_URL'] + lat + "," + lng)
    # print('getGeoInfo > url: ', url)
    result = requests.get(url)
    js = result.json()
    if result.status_code != 200 or len(js['results']) == 0:
        # print(js['status'])
        return None
    # print('getGeoInfo: ', js)
    names = {}
    for i in range(len(js['results'][0]['address_components'])):
        names[js['results'][0]['address_components'][i]['types'][0]] = js['results'][0]['address_components'][i]['long_name']
    return names
            