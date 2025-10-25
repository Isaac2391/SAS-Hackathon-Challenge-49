import sqlite3 as sq
from maps import Search


def initialisedb():
    conn = sq.connect("places.db")

    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS places(
        User_ID TEXT PRIMARY KEY,
        Name Text
    )""")

    conn.commit()
    conn.close()
    
def UserStorage(Name):
    conn = sq.connect("Places.db")
    
    c = conn.cursor()
    
    c.execute("INSERT INTO Places (Name) VALUEs (?)",((Name,)))
    
    conn.commit()
    
    conn.close()
    
    
    
    
