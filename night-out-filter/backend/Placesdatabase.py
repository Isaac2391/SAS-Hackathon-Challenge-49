import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "places.db"
DATA_PATH = Path(__file__).resolve().parent / "data" / "activities.json"

TAG_COLUMNS = ["Social", "Competitive", "Hidden_Gem", "Casual", "Celebration", "Energetic"]

def setup_db():
    # create tables if they don’t exist
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(f"""
        CREATE TABLE IF NOT EXISTS people (
            user_id TEXT PRIMARY KEY,
            {', '.join(f'{t} INTEGER DEFAULT 0' for t in TAG_COLUMNS)}
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS venues (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT,
            base_cost REAL,
            location TEXT,
            tags TEXT
        )
        """)
        conn.commit()
    seed_venues()
    print("Database ready.")

def seed_venues():
    if not DATA_PATH.exists():
        print("activities.json missing.")
        return
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM venues")
        if c.fetchone()[0] > 0:
            return
        venues = json.load(open(DATA_PATH, "r", encoding="utf-8"))
        for v in venues:
            c.execute(
                "INSERT INTO venues (id, name, description, base_cost, location, tags) VALUES (?, ?, ?, ?, ?, ?)",
                (v["id"], v["name"], v["description"], v["base_cost"], v["location"], json.dumps(v["tags"]))
            )
        conn.commit()
        print(f"Seeded {len(venues)} venues.")

def record_vote(user_id: str, venue_id: int, vote: int):
    # record a yes/no (1/0) vote for a venue.
    # yes (1) increments each tag column for that venue in the user's record.

    if vote not in (0, 1):
        raise ValueError("Vote must be 0 (No) or 1 (Yes)")

    if vote == 0:
        return  # No-op for a "No"

    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        # ensure user row
        c.execute("INSERT OR IGNORE INTO people (user_id) VALUES (?)", (user_id,))

        # get venue tags
        c.execute("SELECT tags FROM venues WHERE id=?", (venue_id,))
        row = c.fetchone()
        if not row:
            print(f"Venue {venue_id} not found")
            return
        tags = json.loads(row[0])
        for tag in tags:
            col = tag.replace(" ", "_")
            if col in TAG_COLUMNS:
                c.execute(f"UPDATE people SET {col} = {col} + 1 WHERE user_id=?", (user_id,))
        conn.commit()

def get_venues():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT id, name, description, base_cost, location, tags FROM venues")
        rows = c.fetchall()
    return [
        {
            "id": r[0],
            "name": r[1],
            "description": r[2],
            "base_cost": r[3],
            "location": r[4],
            "tags": json.loads(r[5])
        }
        for r in rows
    ]

def _parse_budget(budget_str: str) -> float:

    if not budget_str:
        return 0  
    
   
    budget_str = budget_str.split('-')[0]
   
    budget_str = budget_str.replace('£', '').replace('+', '')
    
    try:
        return float(budget_str)
    except ValueError:
        return 0

def add_venue(name: str, description: str, base_cost_str: str, location: str, tags_list: list):
    """Inserts a new user-suggested venue into the database."""
    
    base_cost = _parse_budget(base_cost_str)
    
   
    valid_tags = [tag for tag in tags_list if tag] 
    tags_json = json.dumps(valid_tags) 

    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO venues (id, name, description, base_cost, location, tags) VALUES (NULL, ?, ?, ?, ?, ?)",
                (name, description, base_cost, location, tags_json)
            )
            conn.commit()
            print(f"Successfully added new venue: {name}")
        except Exception as e:
            print(f"Error adding venue: {e}")