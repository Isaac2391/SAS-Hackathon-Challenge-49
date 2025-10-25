from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os

app = Flask(__name__)
CORS(app)

# Route to handle form submission
@app.route('/submit_suggestion', methods=['POST'])
def submit_suggestion():
    data = request.get_json()

    # Extract fields from the incoming JSON
    activity_name = data.get('activityName')
    activity_type = data.get('activityType')
    location = data.get('location')
    message = data.get('message')

    # Define the CSV file path
    file_path = 'suggestions.csv'
    file_exists = os.path.isfile(file_path)

    # Write to CSV
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            # Write header if file is new
            writer.writerow(['Activity Name', 'Activity Type', 'Location', 'Message'])
        writer.writerow([activity_name, activity_type, location, message])

    return jsonify({'status': 'success', 'message': 'Suggestion saved successfully!'})

# Run the Flask server
if __name__ == '__main__':
    app.run(debug=True)
print("Flask app is running...")