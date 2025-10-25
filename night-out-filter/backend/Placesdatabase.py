import sqlite3 as sq
from maps import Search


def initialisedb():
    conn = sq.connect("places.db")

    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS places(
        place_ID TEXT PRIMARY KEY NOT NULL,
        Name TEXT,
        Vicinty TEXT,
        Types TEXT,
        Rating REAL,
        User_rating_total INTEGER,
        business_status TEXT,
        lat REAL,
        lng REAL
    )""")

    conn.commit()
    conn.close()
    
def searchandstore(storecat):
    Search(storecat)
    conn = sq.connect("Places.db")
    
    c = conn.cursor
    
    c.execute("INSERT INTO expenses")
    
    
    
    
