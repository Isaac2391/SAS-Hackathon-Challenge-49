from flask import Flask, request, jsonify
from backend.data.recommender import recommend_venues
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json(force=True)
    budget = data.get("budget", 30)
    result = recommend_venues(
        mood=data.get("mood"),
        budget=budget,
        occasion=data.get("occasion")
    )
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
