import json
import random

def load_venues(file_path):
    with open(file_path, 'r') as file:
        venues = json.load(file)
    return venues

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
