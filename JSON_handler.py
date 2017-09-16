

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

def getCategoriesDict ():
    '''
    return a list of dictionaries, with fields as per link below
    https://eonet.sci.gsfc.nasa.gov/docs/v2.1#categoriesAPI

    '''
    
    filePath = os.path.join (os.getcwd(), "EONET_DATA",'categories.json' )
    with open( filePath ) as data_file:    
        data = json.load(data_file)

    return data ['categories']

if __name__ == '__main__' :
    fromDate = datetime.date ( 2017, 9, 1 )
    toDate   = datetime.date.today()
    #d = getEventsDict ( fromDate, toDate )
    #print d
    getCategoriesDict ()
    
