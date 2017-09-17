'''

Script to download data from EONET, put it into a spreadsheet and then to email 
that spreadsheet

'''
import sys
import logging
import os


'''
Create a logger (which I really  found time to use properly)
'''

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('transfer_data.log')
formatter = logging.Formatter('%(asctime)s-%(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Obtain email address

if  len ( sys.argv ) < 2 :
    print "usage: python transfer_EONET.py recipient_name@domain.com"
    sys.exit ()
 
recip_email = sys.argv[1]
print recip_email

import JSON_handler
import db_handler

db_handler.setUpDB()

lstCatDicts = JSON_handler.getCategoriesDict ()
db_handler.loadCategoriesDict (lstCatDicts)

import datetime
from datetime import timedelta
toDate   = datetime.date.today()
fromDate = toDate - timedelta (days = 1 )
lstEventDicts = JSON_handler.getEventsDict ( fromDate, toDate )
db_handler.loadEventsDict (lstEventDicts)

lstResultsforSpreadsheet = db_handler.getEventData ()

import Excel_Handler as eh
eh.createWorkbook ()
eh.writeEvents ( lstResultsforSpreadsheet )

import email_handler

user = "johnsteedman360dev@gmail.com"
pwd   = 'DEVED!23'
subject = 'EONET Events Last 30 days'
body    = 'Please find attached a listing of the EONET global Events limited to Wildfires, Severe Stores and Wilfires as requested. \n Kind regards, John'
excel_file_path = eh.getExcelFilePath ()

excel_file_path =os.path.join (os.getcwd(),'EONET_Events.xlsx' )
email_handler.send_email(user, pwd, recip_email, subject, body, excel_file_path)



