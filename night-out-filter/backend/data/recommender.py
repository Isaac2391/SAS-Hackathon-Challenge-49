# completed the functions so they
#- load venue data from a JSON file,
#- filter venues based on budget, mood, and occasion,
#- calculate an overall fun score (OFS) for each venue,
#- and return the top 5 recommended venues.

import json
import random
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent / "activities.json"

def load_venues(file_path: str | None = None):
    p = Path(file_path) if file_path else DATA_PATH
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

def filter_by_budget(venues, budget: float | int):
    try:
        b = float(budget)
    except (TypeError, ValueError):
        b = 30
    return [v for v in venues if float(v.get("base_cost", 0)) <= b]

def filter_by_mood(venues, mood: str | None):
    if not mood:
        return venues
    mood = mood.strip().lower()
    return [v for v in venues if mood in [t.lower() for t in v.get("tags", [])]]

def filter_by_occasion(venues, occasion: str | None):
    if not occasion:
        return venues
    occasion = occasion.strip().lower()
    return [v for v in venues if occasion in [t.lower() for t in v.get("tags", [])]]

def calculate_ofs(venue, mood, budget, occasion):
    score = 5
    tags = [t.lower() for t in venue.get("tags", [])]
    if mood and mood.lower() in tags: score += 2
    if occasion and occasion.lower() in tags: score += 2
    try:
        if float(budget) >= float(venue.get("base_cost", 0)): score += 1
    except (TypeError, ValueError):
        pass
    score += random.randint(0, 2)
    return min(score, 10)

def get_recommendations(mood=None, budget=30, occasion=None, file_path=None):
    venues = load_venues(file_path)
    filtered = filter_by_budget(venues, budget)
    filtered = filter_by_mood(filtered, mood)
    filtered = filter_by_occasion(filtered, occasion)
    for v in filtered:
        v["ofs"] = calculate_ofs(v, mood, budget, occasion)
    return sorted(filtered, key=lambda x: x["ofs"], reverse=True)[:5]

