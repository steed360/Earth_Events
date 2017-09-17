import json, urllib2
import datetime
import os

def getEventsDict ( fromDate = datetime.date.today(), toDate= datetime.date.today() ):
 
    '''
    return a list of event dictionaries, with fields as per link below
    https://eonet.sci.gsfc.nasa.gov/docs/v2.1#eventsAPI

    @dateFrom   
    @dateTo  

    '''

    daysSince =   ( toDate - fromDate  ).days + 1

    url =   "https://eonet.sci.gsfc.nasa.gov/api/v2.1/events?days=%s" %( daysSince )
    # 	&limit=100&status=open
    data = json.load (urllib2.urlopen (url) )
    list_of_dicts = data ['events']
    return list_of_dicts

#def getEventsDict ( daysSince = 1 ):
#    from datetime import timedelta
#    toDate   = datetime.date.today()
#   fromDate = toDate - timedelta ( daysSince )
#   return getEventsDict ( fromDate, toDate)  File "/home/john/CODE/EONET_BASICS/JSON_handler.py", line 77




def getCategoriesDict ():
    '''
    return a list of dictionaries, with fields as per link below
    https://eonet.sci.gsfc.nasa.gov/docs/v2.1#categoriesAPI

    '''
    
    filePath = os.path.join (os.getcwd(), "EONET_DATA",'categories.json' )
    with open( filePath ) as data_file:    
        data = json.load(data_file)

    return data ['categories']

def getCountryForLatLon (lat, lon):
    '''


    Uses the google API
    c.f. https://stackoverflow.com/questions/4013606/google-maps-how-to-get-country-state-province-region-city-given-a-lat-long-va
    '''
    url = "http://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&sensor=false" %(lat,lon)


    try:
        data = json.load (urllib2.urlopen (url) )
        lstFirstResultAddr =  data ['results'][0]['address_components']

        #brings back 
        '''
    "address_components" : [
            {
               "long_name" : "231",
               "short_name" : "231",
               "types" : [ "street_number" ]
            },
            {
               "long_name" : "South 3rd Street",
               "short_name" : "S 3rd St",
               "types" : [ "route" ]
            },  etc
        '''

        resDict = [thisDict for thisDict in lstFirstResultAddr if  'country' in thisDict['types']] 
        return resDict.pop () ['long_name'] 
    except Exception as e:
        print "Cannot use maps.googleapis.com latlong country result for %s, %s" %(lat,lon)
        print e
        return "Not Known"


if __name__ == '__main__' :
    res = getCountryForLatLon ( 49.0267333,  -117.3498 )
    print res

    res = getCountryForLatLon (  40.7110, -73.95831 )
    print res

    fromDate = datetime.date ( 2017, 9, 1 )
    toDate   = datetime.date.today()
    #d = getEventsDict ( fromDate, toDate )
    #print d
    #getCategoriesDict ()
    
