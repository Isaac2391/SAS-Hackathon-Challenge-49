# changes made by simi: weekend column changed to celebration column, made people and venues live in same db, changed table name from places to people as we have a places table for venues, 
import sqlite3 as sq

def initialisedb():
    conn = sq.connect("places.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS people(
            user_id TEXT PRIMARY KEY,
            name TEXT DEFAULT 'ANONYMOUS_USER',
            social INTEGER DEFAULT 0,
            competitive INTEGER DEFAULT 0, 
            hidden_gem INTEGER DEFAULT 0, 
            casual INTEGER DEFAULT 0, 
            celebration INTEGER DEFAULT 0, 
            energetic INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()

def add_user(user_id, name, social, competitive, hidden_gem, casual, celebration, energetic):
    conn = sq.connect("places.db")
    c = conn.cursor()

    c.execute("""
        INSERT OR REPLACE INTO people 
        (user_id, name, social, competitive, hidden_gem, casual, celebration, energetic)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, name, social, competitive, hidden_gem, casual, celebration, energetic))

    conn.commit()
    conn.close()

def display_database():
    conn = sq.connect("places.db")
    c = conn.cursor()

    c.execute("SELECT * FROM people")
    all_entries = c.fetchall()

    print("\n--- People Database ---")
    for entry in all_entries:
        print(entry)

    conn.close()
    display_database()
