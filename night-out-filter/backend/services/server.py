
from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="mydb",
    user="username",
    password="password",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# fetch all cards with optional filtering
@app.route("/cards", methods=["GET"])
def get_cards():
    mood = request.args.get("mood")
    budget = request.args.get("budget", type=float)
    type_ = request.args.get("type")

    cur.execute("SELECT id, tags, price FROM cards")
    cards = cur.fetchall()

    filtered = []
    for card in cards:
        card_id, tags, price = card
        if mood and mood not in tags:
            continue
        if budget and price != budget:
            continue
        if type_ and type_ not in tags:
            continue
        filtered.append({"id": card_id, "tags": tags, "price": price})

    return jsonify(filtered)

# like a card
@app.route("/like", methods=["POST"])
def like_card():
    data = request.json
    user_name = data["user_name"]
    card_id = data["card_id"]

    # get or create user
    cur.execute("SELECT user_id FROM users WHERE name=%s", (user_name,))
    user = cur.fetchone()
    if not user:
        cur.execute("INSERT INTO users(name) VALUES(%s) RETURNING user_id", (user_name,))
        user_id = cur.fetchone()[0]
        conn.commit()
    else:
        user_id = user[0]

    # insert liked card
    try:
        cur.execute(
            "INSERT INTO liked_cards(user_id, card_id) VALUES(%s, %s)",
            (user_id, card_id)
        )
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()  # card already liked, ignore

    return jsonify({"success": True})

# get top 5 recommendations
@app.route("/recommend/<user_name>", methods=["GET"])
def recommend(user_name):
    # Get user
    cur.execute("SELECT user_id FROM users WHERE name=%s", (user_name,))
    user = cur.fetchone()
    if not user:
        return jsonify([])
    user_id = user[0]

    # get liked cards
    cur.execute("SELECT card_id FROM liked_cards WHERE user_id=%s", (user_id,))
    liked_rows = cur.fetchall()
    liked_card_ids = [r[0] for r in liked_rows]
    if not liked_card_ids:
        return jsonify([])

    # get tags of liked cards
    cur.execute("SELECT tags FROM cards WHERE id IN %s", (tuple(liked_card_ids),))
    liked_cards = cur.fetchall()

    tag_map = {}
    for card in liked_cards:
        for tag in card[0]:
            tag_map[tag] = tag_map.get(tag, 0) + 1

    # score all cards
    cur.execute("SELECT id, tags, price FROM cards")
    all_cards = cur.fetchall()
    scored_cards = []
    for card in all_cards:
        card_id, tags, price = card
        if card_id in liked_card_ids:
            continue
        score = sum(tag_map.get(tag, 0) for tag in tags)
        scored_cards.append({"id": card_id, "tags": tags, "price": price, "score": score})

    # top 5
    scored_cards.sort(key=lambda x: x["score"], reverse=True)
    top5 = scored_cards[:5]

    return jsonify(top5)

if __name__ == "__main__":
    app.run(debug=True, port=3000)
