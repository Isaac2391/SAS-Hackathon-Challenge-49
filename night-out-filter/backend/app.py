from flask import Flask, request, jsonify
from data.recommender import get_recommendations

app = Flask(__name__)

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    result = get_recommendations(
        mood=data.get("mood"),
        budget=data.get("budget", 30),
        occasion=data.get("occasion")
    )
    return jsonify(result)

app.run(debug=True)
