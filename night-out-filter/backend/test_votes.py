import Placesdatabase as pb

print("Recording sample votes...")

# Simulate some employee votes
pb.record_vote("alice", 1, 1)     # Alice likes "Flight Club Glasgow"
pb.record_vote("bob", 3, 1)       # Bob likes "Boom Battle Bar"
pb.record_vote("charlie", 5, 1)   # Charlie likes "Escape Glasgow"

print("Votes recorded successfully!")

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "places.db"
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

print("\nPeople table contents:")
for row in c.execute("SELECT * FROM people;"):
    print(" ", row)

conn.close()
print("\nDone.")
