import sqlite3 as sq

def initialisedb():
    conn = sq.connect("places.db")

    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS places(
        User_ID TEXT PRIMARY KEY,
        Name Text,
        Social Text,
        Competitive Text, 
        HiddenGem Text, 
        Casual Text, 
        Celebration Text, 
        Energetic Text
    )""")
     

    conn.commit()
    conn.close()
    
def UserStorage(Name):
    conn = sq.connect("Places.db")
    
    c = conn.cursor()
    
    c.execute("INSERT INTO Places (Name) VALUEs (?)",((Name,)))
    
    conn.commit()
    
    conn.close()

