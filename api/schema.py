import datetime, json

class Disease():
    def __init__(self):
            self.name = ''
            self.description = ''
            self.remedyName = ''
    
    def jsonable(self):
        return self.__dict__
    
class Remedy():
    def __init__(self):
            self.name = ''
            self.description = ''
            self.medicine = ''
            self.dose = ''
            self.remarks = ''

    def jsonable(self):
        return self.__dict__    

class Geocode():
    def __init__(self):
            self.lat = ''
            self.lng = ''

    def jsonable(self):
        return self.__dict__    
        
class Location():
    def __init__(self): 
        self.geocode = ''
        self.disease = ''
        self.pincode = ''
        self.city = ''
        self.state = ''
        self.country = ''
        self.createdOn = str(datetime.datetime.utcnow())

    def jsonable(self):
        return self.__dict__
        
class Prediction():
    def __init__(self):
        self.status = False
        self.message = ''
        self.disease = ''
        self.remedy = ''
        self.confidence = ''

    def jsonable(self):
        return self.__dict__    
        
def ComplexHandler(Obj):
    if hasattr(Obj, 'jsonable'):
        return Obj.jsonable()
    else:
        raise TypeError('Object of type %s with value of %s is not JSON serializable' % (type(Obj), repr(Obj)))
        