import sqlite3
from pathlib import Path

print("Starting test_db.py...")

DB_PATH = Path(__file__).resolve().parent / "places.db"

print(f"Looking for database at: {DB_PATH}")
if not DB_PATH.exists():
    print("Database file not found!")
    exit()

try:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    print("\nConnected successfully!\n")

    print("Tables in database:")
    for row in c.execute("SELECT name FROM sqlite_master WHERE type='table';"):
        print(" -", row[0])

    print("\nSample venues:")
    for row in c.execute("SELECT id, name, location FROM venues LIMIT 5;"):
        print(" ", row)

    print("\nPeople table:")
    for row in c.execute("SELECT * FROM people;"):
        print(" ", row)

    conn.close()
    print("\nDone.")

except Exception as e:
    print(f"Error: {e}")
