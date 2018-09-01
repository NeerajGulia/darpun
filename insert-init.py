from api import mongo, utils
from api.schema import Disease, Remedy, ComplexHandler
import csv, json

def insertDisease(name):
    if not mongo.db.diseases.find_one({'name' : name}):
        d = Disease()
        d.name = name
        d.description = 'description for ' + name
        d.remedyName = 'Remedy for ' + name
        d = utils.getJson(d)
        mongo.db.diseases.insert(d)
    
def insertRemedy(disease, remedyDescription):
    remedyName = 'Remedy for ' + disease
    if not mongo.db.remedies.find_one({'name' : remedyName}):
        r = Remedy()
        r.name = remedyName
        r.description = remedyDescription
        r.medicine = ''
        r.dose = ''
        r.remarks = ''
        r = utils.getJson(r)
        mongo.db.remedies.insert(r)
    
with open('crowdai_labels.csv') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        insertDisease(line[0])
        insertRemedy(line[0], line[1])
        print('inserted: ', line[0])