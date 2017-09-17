import os
import sqlite3
import pprint

db_path =    os.path.join (os.getcwd(),'event_db' )

Event_DDL = '''
       CREATE TABLE Events ( 
          id                   TEXT,
          title                TEXT,
          description          TEXT,
          link                 TEXT,
          categories_text      TEXT,
          PRIMARY KEY (ID)
       )
     '''

Categories_DDL = '''
    CREATE TABLE Categories (
       category_id           TEXT, 
       category_title        TEXT,
       category_description  TEXT, 
       category_layers       TEXT,
       category_link         TEXT
    )
'''

Event_Categories_DDL = '''
     CREATE TABLE Event_Categories (
        event_id              TEXT,
        category_id           TEXT
   )
'''

def setUpDB ():

    if (os.path.exists (db_path) ):
        os.remove(  db_path)
        # logger.info ("removed database")

    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    cursor.execute( Event_DDL)
    cursor.execute( Categories_DDL)
    cursor.execute (Event_Categories_DDL )

    db.commit()
    db.close()   


def loadEventsDict (eventsDictList):

    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    
    for anEventDict in  eventsDictList:

        eventCats = anEventDict['categories']

        lstCategories = []
        for aCategoryDict in eventCats:
            # flatten out the potentially multiple categories into a list             
            lstCategories.append (aCategoryDict['title'])
            # also preserve the many-many relationship with the categories reference table.
            sqlStr = " insert into Event_Categories ( category_id, event_id ) values ('%s', '%s') " %(aCategoryDict ['id'], anEventDict['id'])
            #print sqlStr
            cursor.execute (sqlStr )

        categoriesTxt = ','.join ( lstCategories )

        if (len ( lstCategories ) > 1 ) : 
            print categoriesText

        print lstCategories

        sqlStr = "insert into Events (id, title, description, link,categories_text ) values ('%s', '%s', '%s', '%s', '%s')" %( anEventDict['id'], anEventDict['title'], anEventDict['description'],anEventDict['link'], categoriesTxt  )
        cursor.execute (sqlStr )


    db.commit()
    db.close()   

def loadCategoriesDict (categoriesDictList):

    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    
    for aCat  in  categoriesDictList:

        sqlStr = "insert into Categories (category_id, category_title, category_description, category_layers, category_link ) values ('%s', '%s', '%s', '%s', '%s')" %( aCat['id'], aCat['title'], aCat['description'],aCat['layers'], aCat['link'] )

        # print sqlStr

        cursor.execute (sqlStr )

    db.commit()
    db.close()   


def viewRows (SQL):
    db = sqlite3.connect(db_path)
    cursor = db.cursor()
  
    cursor.execute(SQL)
 
    rows = cursor.fetchall()
 
    for row in rows:
        #pprint (row)
        print row
if __name__ == '__main__' :
    setUpDB()
    
    import JSON_handler, datetime
    d = JSON_handler.getEventsDict (datetime.date (2017,3,1), datetime.date.today() )

    loadEventsDict (d)

    c = JSON_handler.getCategoriesDict ()
    loadCategoriesDict (c)

    SQL =    ''' 
select * 
from Events e 
'''
    #viewRows ( SQL) 




