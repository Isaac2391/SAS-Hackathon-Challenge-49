import json
import random

# Load venues from JSON file
def load_venues(file_path="backend/data/activities.json"):
    with open(file_path, 'r') as file:
        venues = json.load(file)
    return venues

# Filter functions
def filter_by_budget(venues, budget):
    return [v for v in venues if v["base_cost"] <= budget]

# Filter by mood
def filter_by_mood(venues, mood):
    if not mood:
        return venues
    return [v for v in venues if mood in v["tags"]]

def filter_by_occasion(venues, occasion):
    if not occasion:
        return venues
    return [v for v in venues if occasion in v["tags"]]

# Calculate Office Fun Score (OFS)
def calculate_ofs(venue, mood, budget, occasion):
    score = 5  # base score
    if mood in venue["tags"]:
        score += 2  # extra points for matching mood
    if occasion in venue["tags"]:
        score += 2  # extra points for matching occasion
    if budget >= venue["base_cost"]:
        score += 1  # extra points if affordable
    score += random.randint(0, 2)  # small random variation
    return min(score, 10)  # cap at 10

# Main recommendation function
def get_recommendations(mood=None, budget=30, occasion=None, file_path="activities.json"):
    venues = load_venues(file_path)

    # Apply filters
    filtered = filter_by_budget(venues, budget)
    filtered = filter_by_mood(filtered, mood)
    filtered = filter_by_occasion(filtered, occasion)

    # Score each venue
    for v in filtered:
        v["ofs"] = calculate_ofs(v, mood, budget, occasion)

    # Sort by fun score and return top 5
    top5 = sorted(filtered, key=lambda x: x["ofs"], reverse=True)[:5]
    return top5

