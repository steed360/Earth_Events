'''
Incomplete script that loads one of the EONET tables into an SQLlite database.
'''

import json, urllib2
import sqlite3
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

'''
 create a file handler
'''

handler = logging.FileHandler('transfer_data.log')
formatter = logging.Formatter('%(asctime)s-%(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

url =  "https://eonet.sci.gsfc.nasa.gov/api/v2.1/events?days=30"  
# 	&limit=100&status=open

'''
Connect to the data
'''

data = json.load (urllib2.urlopen (url) )
list_of_dicts = data ['events']
logger.info ("There are %s records",len(list_of_dicts) )

eventDict = list_of_dicts [0]


''' 
Filter out the categories that are of no interest
'''
#  Specify categories of interest. I'm assuming Earthquakes and landslips are different entities. 
#  relevCats = ['Severe Storms', 'Wildfires', 'Earthquakes']  c.f. examination.py

relevCatsSet = set (  ['Severe Storms', 'Wildfires'])

lstEventsFiltered = []

for anEvent in list_of_dicts:
    categortTitlesSet = set()
    for anEventCategoryDict in anEvent['categories']:
        categortTitlesSet.add ( anEventCategoryDict['title'] )
    relevCatsFound =  categortTitlesSet.intersection (relevCatsSet  )
    if ( len  ( relevCatsFound ) > 0):
        lstEventsFiltered.append ( anEvent )


'''
Create a basic SQL database
'''

db_path = os.path.join (os.getcwd(), 'event_db' )
if (os.path.exists (db_path) ):
    os.remove(  db_path)
    logger.info ("removed database")


db = sqlite3.connect('event_db')

cursor = db.cursor()

cursor.execute('''
   CREATE TABLE Events (
   id             TEXT,
   title          TEXT,
   description    TEXT,
   link           TEXT,
   PRIMARY KEY (ID)
   )
''')



#TODO : Add date range from geom table


db.commit()

'''
Insert the data into the database
'''

for anEvent in  lstEventsFiltered:

    sqlStr = "insert into Events (id, title, description, link ) values ('%s', '%s', '%s', '%s')" %( anEvent['id'], anEvent['title'], anEvent['description'],anEvent['link'] )

    cursor.execute (sqlStr )


# cursor = db.cursor()
db.commit()
db.close()






