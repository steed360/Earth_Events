import os
import sqlite3

db_path =    os.path.join (os.getcwd(),'event_db' )

Event_DDL = '''
       CREATE TABLE Events (
          id             TEXT,
          title          TEXT,
          description    TEXT,
          link           TEXT,
          category_ID    TEXT,
          PRIMARY KEY (ID)
       )
     '''

Categories_DDL = '''
    CREATE TABLE Categories (
       category_id           TEXT, 
       category_title        TEXT,
       category_description  TEXT, 
       category_layers       TEXT
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

    print 'd'

    db.commit()
    db.close()   


def loadEventsDict (eventsDictList):

    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    
    for anEvent in  eventsDictList:

        sqlStr = "insert into Events (id, title, description, link ) values ('%s', '%s', '%s', '%s')" %( anEvent['id'], anEvent['title'], anEvent['description'],anEvent['link'] )

        cursor.execute (sqlStr )

    db.commit()
    db.close()   

if __name__ == '__main__' :
    setUpDB()
    
    import JSON_handler
    d = JSON_handler.getEventsDict ()

    loadEventsDict (d)
     
     
     

