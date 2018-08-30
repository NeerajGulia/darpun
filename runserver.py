from api import app
app.run(debug=False)

# import json, requests

# GEO_URL = "https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyBNyP78_OKJpgCNMPqASTlWuOOQOFf94WY&latlng="

# def getGeoInfo(location):
    # url = GEO_URL + location
    # result = requests.get(url)
    # js = result.json()
    # if result.status_code != 200 or len(js['results']) == 0:
        # print(js['status'])
        # return None
    # names = {}
    # for i in range(len(js['results'][0]['address_components'])):
        # names[js['results'][0]['address_components'][i]['types'][0]] = js['results'][0]['address_components'][i]['long_name']
    # return names

# long, lat = 10.300970, 76.650874
# for i in range(10):
    # code = str(long + i) + "," + str(lat + i)
    # print('code: ', code)
    # output = getGeoInfo(code)
    # if output != None:
        # pincode = output.get('postal_code', None)
        # city = output.get('administrative_area_level_2', None)
        # state = output.get('administrative_area_level_1', None)
        # country = output.get('country', None)
        # if pincode == None or city == None or state == None or country == None:
            # continue
        # print('pin: {}, city: {}, state: {}, country: {}'.format(pincode, city, state, country))
    