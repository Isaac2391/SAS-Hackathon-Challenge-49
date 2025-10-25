import json

cards = []
with open('activities.json', 'r') as file:
    data = json.load(file)
for card in data:
    cards.append(card)

user_filters = {
    "mood": "chill",
    "budget": "Low",
    "activity_type": "trivia"
}

def filter_cards(cards, filters):
    filtered = []

    for card in cards:
        if filters.get("mood") and filters["mood"] not in card["tags"]:
            continue

        if filters.get("budget") and filters["budget"] != card.get("price"):
            continue

        if filters.get("activity_type") and filters["activity_type"] not in card["tags"]:
            continue

        filtered.append(card)
    
    return filtered

swipe_deck = filter_cards(cards, user_filters)


if not swipe_deck:
    print("No results found, try changing your filters.")
else:
    print("Swipe deck ready! Cards to show:")
    for card in swipe_deck:
        print(f"- {card['name']} ({card['price']}) - Tags: {card['tags']}")
