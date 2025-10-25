import sqlite3 as sq

def initialisedb():
    conn = sq.connect("places.db")

    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS places(
        User_ID TEXT PRIMARY KEY,
        Name TEXT DEFAULT ANONYMOUS_USER,
        Social INTEGER DEFAULT 0,
        Competitive INTEGER DEFAULT 0, 
        HiddenGem INTEGER DEFAULT 0, 
        Casual INTEGER DEFAULT 0, 
        Celebration INTEGER DEFAULT 0, 
        Energetic INTEGER DEFAULT 0
    )""")
     
    conn.commit()
    conn.close()

def UserStorage(user_id, name, social, competitive, hidden_gem, casual, weekend, energetic):
    conn = sq.connect("places.db")
    c = conn.cursor()
    
    c.execute("""INSERT INTO places 
                (user_id, name, social, competitive, hidden_gem, casual, weekend, energetic) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (user_id, name, social, competitive, hidden_gem, casual, weekend, energetic))
    
    conn.commit()
    conn.close()

def display_database():
    conn = sq.connect("places.db")
    c = conn.cursor()
    
    c.execute("SELECT * FROM places")
    all_entries = c.fetchall()
    
    for entry in all_entries:
        print(entry)
    
    conn.close()

display_database() 