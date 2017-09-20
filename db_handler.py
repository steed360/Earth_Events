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
          country              TEXT,
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

Event_Geometry_DDL = '''
     CREATE TABLE Event_Geometry (
        event_id              TEXT,
        geom_date             DATETIME,
        geometry_type         TEXT,
        coordinates           TEXT
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
    cursor.execute (Event_Geometry_DDL )

    db.commit()
    db.close()   


def filterEventDictList (lstEventDicts):


    ''' 
    This function goes through the JSON structure of events and filters them
    However, while it works, it is not used as it seemed better to do filtering in 
    the database, since we're using one.
    '''

    
    #  in examination.py several years of data was looked at in fact no landslides were found.
    #  relevCats = ['Severe Storms', 'Wildfires', 'Earthquakes']  

    relevCatsSet = set (  ['Severe Storms', 'Wildfires','Landslides'])

    lstEventsFiltered = []

    for anEvent in list_of_dicts:
        categortTitlesSet = set()
        for anEventCategoryDict in anEvent['categories']:
            categortTitlesSet.add ( anEventCategoryDict['title'] )
        relevCatsFound =  categortTitlesSet.intersection (relevCatsSet  )
        if ( len  ( relevCatsFound ) > 0):
            lstEventsFiltered.append ( anEvent )
    return lstEventsFiltered



def loadEventsDict (eventsDictList):

    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    
    for anEventDict in  eventsDictList:

        eventCats = anEventDict['categories']

        # Grab the first set of co-ordinates in the Geometry dictionary and use it 
        # to find the country

        firstGeomDict = anEventDict['geometries'][0]
        if firstGeomDict['type'] == 'Point':
            # "coordinates": [ 146.90, 13.40 ]
            lat =  firstGeomDict['coordinates'][1] 
            lon =  firstGeomDict['coordinates'][0]
             
        if firstGeomDict['type'] == 'Polygon':
            # coordinates": [[ [1.34765625, 12.011583667128816], [1.34765625, 15.52480746148673]..
            lat =  firstGeomDict['coordinates'][0][0][1] 
            lon =  firstGeomDict['coordinates'][0][0][0] 
        import JSON_handler
        country = JSON_handler.getCountryForLatLon (lat, lon)

        # handle repeating categories
        lstCategories = []
        for aCategoryDict in eventCats:
            # flatten out the potentially multiple categories into a list             
            lstCategories.append (aCategoryDict['title'])
            # also preserve the many-many relationship with the categories reference table.
            sqlStr = " insert into Event_Categories ( category_id, event_id ) values ('%s', '%s') " %(aCategoryDict ['id'], anEventDict['id'])
            #print sqlStr
            cursor.execute (sqlStr )

        categoriesTxt = ','.join ( lstCategories )


        sqlStr = "insert into Events (id, title, description, link,categories_text,country ) values ('%s', '%s', '%s', '%s', '%s','%s')" %( anEventDict['id'], anEventDict['title'], anEventDict['description'],anEventDict['link'],categoriesTxt,country  )
        #print sqlStr
        cursor.execute (sqlStr )


    db.commit()
    db.close()   

def loadEventGeometries ( lstEventDicts):

    db = sqlite3.connect(db_path)
    cursor = db.cursor()

    for anEventDict in  lstEventDicts:

        for aGeomDict in anEventDict ['geometries']:
            
            SQL = ''' insert into Event_Geometry ( event_id, geom_date, geometry_type,
                       coordinates )
                      values ( '%s', '%s','%s','%s' ) ''' %(anEventDict['id'],aGeomDict['date'], aGeomDict['type'], aGeomDict['coordinates'] )

            cursor.execute (SQL)
    db.commit ()
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


def getEventData ():
    SQL = '''
       select e.id, e.title, e.description, e.link, e.categories_text, e.country, 
              min (date(eg.geom_date )) as earliest_date,
              max (date(eg.geom_date )) as latest_date 
       from Events e
       inner join Event_Categories ec on ( e.id = ec.event_id )
       inner join Categories c  on ( ec.category_id = c.category_id ) 
       left join Event_Geometry  eg on ( e.id = eg.event_id )
       where c.category_title in  ( 'Severe Storms', 'Wildfires','Landslides' )
       group by e.id, e.title, e.description, e.link, e.categories_text, e.country

    '''



    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    cursor.execute( SQL)
 
    return   cursor.fetchall()


if __name__ == '__main__' :


    setUpDB()

    import JSON_handler, datetime
    d = JSON_handler.getEventsDict (datetime.date (2017,9,19), datetime.date.today() )
    # d = JSON_handler.getEventsDict (2 )

    loadEventsDict (d)
    loadEventGeometries (d)

    c = JSON_handler.getCategoriesDict ()
    loadCategoriesDict (c)

    SQL =    ''' 
select *  
from Event_Geometry 
'''

    #viewRows ( SQL) 


    dat = getEventData ()
    print dat



