import sqlite3
from pathlib import Path
import Placesdatabase as pb  # lowercase import (case-sensitive on some systems)

DB_PATH = Path(__file__).resolve().parent / "places.db"

pb.setup_db()

def get_team_preferences():
    # pull all users from the people table and average their traits
    conn = sqlite3.connect("DB_PATH")
    c = conn.cursor()

    c.execute("SELECT Social, Competitive, Hidden_Gem, Casual, Celebration, Energetic FROM people")

    rows = c.fetchall()
    conn.close()

    if not rows:
        print("No user data found.")
        return None

    # average each category
    totals = [0] * 6
    for row in rows:
        for i, val in enumerate(row):
            totals[i] += val

    num_users = len(rows)
    averages = [round(t / num_users, 2) for t in totals]

    tags = ["social", "competitive", "hidden_gem", "casual", "celebration", "energetic"]
    team_profile = dict(zip(tags, averages))

    print("Team average preferences:")
    for k, v in team_profile.items():
        print(f"  {k.capitalize()}: {v}")

    return team_profile


def suggest_venues():
    # find venues that best match the team’s average personality."""
    team_profile = get_team_preferences()
    if not team_profile:
        return []

    venues = pb.get_venues()

    # simple scoring: +1 for each tag that matches a top trait
    sorted_traits = sorted(team_profile.items(), key=lambda x: x[1], reverse=True)
    top_traits = [t[0] for t in sorted_traits[:3]]  # top 3 personality tags

    ranked = []
    for v in venues:
        score = 0
        for tag in v["tags"]:
            if tag.lower() in top_traits:
                score += 1
        ranked.append((score, v))

    # sort by score, descending
    ranked.sort(key=lambda x: x[0], reverse=True)

    best = [r[1] for r in ranked if r[0] > 0]
    print(f"🏆 Found {len(best)} matching venues for team profile")
    return best


def generate_html_output():
    # create a basic HTML page showing the top 5 suggested venues."""
    suggestions = suggest_venues()
    if not suggestions:
        print("No suggestions available.")
        return

    html = """
    <html>
    <head>
        <title>Final Suggested Venues</title>
        <style>
            body { font-family: Arial; margin: 40px; background: #fafafa; }
            h1 { text-align: center; }
            .venue { background: white; padding: 15px; margin: 10px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
            img { width: 100%; max-height: 200px; object-fit: cover; border-radius: 10px; }
        </style>
    </head>
    <body>
        <h1>🏁 Final Suggested Venues</h1>
    """

    for v in suggestions[:5]:
        html += f"""
        <div class="venue">
            <h2>{v['name']}</h2>
            <p>{v['description']}</p>
            <p><b>Tags:</b> {', '.join(v['tags'])}</p>
        </div>
        """

    html += "</body></html>"

    with open("frontend/finalsuggestedvalues.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("finalsuggestedvalues.html created successfully!")

if __name__ == "__main__":
    generate_html_output()
