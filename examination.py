

'''
Some rough checks on the data.
'''

import json, urllib2
import sqlite3
import logging
import os

url =  "https://eonet.sci.gsfc.nasa.gov/api/v2.1/events?days=10000"



## Find the distinct set of categories


data = json.load (urllib2.urlopen (url) )
list_of_dicts = data ['events']


data = json.load (urllib2.urlopen (url) )
list_of_dicts = data ['events']

lst_cats = [events['categories'] for events in list_of_dicts]
# print lst_cats
cats = set ()

for cat_Dict_lst in lst_cats:
   for aDict in cat_Dict_lst:
       cats.add ( aDict ['title'] )

print cats 
#>> set([u'Wildfires', u'Severe Storms', u'Earthquakes', u'Sea and Lake Ice', u'Volcanoes'])



