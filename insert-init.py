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
    
def insertRemedy(name):
    if not mongo.db.remedies.find_one({'name' : name}):
        r = Remedy()
        r.name = 'Remedy for ' + name
        r.description = 'Description for ' + name
        r.medicine = 'Medicine for ' + name
        r.dose = 'Dose for ' + name
        r.remarks = 'Remarks for ' + name
        r = utils.getJson(r)
        mongo.db.remedies.insert(r)
    
with open('predict/label_names.csv') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        insertDisease(line[0])
        insertRemedy(line[0])
        print('inserted: ', line[0])