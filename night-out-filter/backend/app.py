from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Save simple suggestions to a CSV under backend/data/
CSV_PATH = Path(__file__).resolve().parent / "suggestions.csv"

@app.post("/submit_suggestion")
def submit_suggestion():
    data = request.get_json(force=True) or {}

    activity_name = data.get("activityName", "").strip()
    activity_type = data.get("activityType", "").strip()
    location = data.get("location", "").strip()
    message = data.get("message", "").strip()

    # basic validation
    if not activity_name:
        return jsonify({"status": "error", "message": "Activity name is required"}), 400

    file_exists = CSV_PATH.exists()
    with CSV_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Activity Name", "Activity Type", "Location", "Message"])
        writer.writerow([activity_name, activity_type, location, message])

    return jsonify({"status": "success", "message": "Suggestion saved successfully!"})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
