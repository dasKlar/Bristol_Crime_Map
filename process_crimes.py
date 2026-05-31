import json
from collections import defaultdict


try:
    with open("cleaned_crimes_bristol.json", "r", encoding="utf-8") as file:
        crimes = json.load(file)
except FileNotFoundError:
    print("Error: cleaned_crimes_bristol.json not found! Please run clean_crimes.py first.")
    exit()


crime_weights = {
    "violent-crime": 7,
    "robbery": 6,
    "possession-of-weapons": 5,
    "burglary": 5,
    "theft-from-the-person": 4,
    "vehicle-crime": 3,
    "drugs": 2,
    "public-order": 2,
    "criminal-damage-arson": 3,
    "other-theft": 1,
    "shoplifting": 1,
    "anti-social-behaviour": 1,
    "bicycle-theft": 1,
    "other-crime": 1
}


street_scores = defaultdict(lambda: {
    "street": "",
    "lat": 0,
    "lng": 0,
    "total_crimes": 0,
    "risk_score": 0,
    "crime_types": defaultdict(int)
})


for crime in crimes:
    key = f"{crime['street']}_{crime['lat']}_{crime['lng']}"
    category = crime["category"]
    weight = crime_weights.get(category, 1)

    street_scores[key]["street"] = crime["street"]
    street_scores[key]["lat"] = crime["lat"]
    street_scores[key]["lng"] = crime["lng"]
    street_scores[key]["total_crimes"] += 1
    street_scores[key]["risk_score"] += weight
    street_scores[key]["crime_types"][category] += 1

results = []


for key, data in street_scores.items():
    score = data["risk_score"]

    if score >= 100:
        level = "high"
    elif score >= 30:
        level = "medium"
    else:
        level = "low"

    results.append({
        "location_key": key,
        "street": data["street"],
        "lat": data["lat"],
        "lng": data["lng"],
        "total_crimes": data["total_crimes"],
        "risk_score": score,
        "risk_level": level,
        "crime_types": dict(data["crime_types"])
    })


results.sort(key=lambda x: x["risk_score"], reverse=True)

# 5. Save the customized results
with open("risk_bristol.json", "w", encoding="utf-8") as file:
    json.dump(results, file, indent=2, ensure_ascii=False)

print(f"Success: Risk locations generated: {len(results)}")
print("-" * 50)
print("Top 10 Most Risky Locations in Bristol (Custom Weights):")
for item in results[:10]:
    print(f"{item['street']} | Score: {item['risk_score']} | Level: {item['risk_level'].upper()}")