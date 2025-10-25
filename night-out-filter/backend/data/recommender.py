import json
import random

#function to load venues from our JSON file
def load_venues(file_path):
    with open(file_path, 'r') as file:
        venues = json.load(file)
    return venues

#function to filter venues by budget and mood
def filter_by_budget(venues, budget):
    return [v for v in venues if v["base_cost"] <= budget]

def filter_by_mood(venues, mood):
    return [v for v in venues if mood in v["tags"]]

#Calculate Office Fun Score
def calculate_ofs(venue, mood, budget):
    score = 5  # base score
    if mood in venue["tags"]:
        score += 2  # extra points for matching mood
    if budget >= venue["base_cost"]:
        score += 1  # extra points if affordable
    score += random.randint(0, 2)  # optional variety
    return min(score, 10)  # cap at 10

#Main recommendation function
def get_recommendations(mood, budget, occasion):
    venues = load_venues()
    
    # Apply filters
    filtered = filter_by_budget(venues, budget)
    filtered = filter_by_mood(filtered, mood) if filtered else venues

    # Score each venue
    for v in filtered:
        v["ofs"] = calculate_ofs(v, mood, budget)
    
    # Sort by fun score and return top 5
    top5 = sorted(filtered, key=lambda x: x["ofs"], reverse=True)[:5]

    return top5


