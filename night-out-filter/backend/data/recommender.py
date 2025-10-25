import json
import random

def load_venues(file_path):
    with open(file_path, 'r') as file:
        venues = json.load(file)
    return venues