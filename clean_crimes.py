import json

try:
    with open("crimes_bristol.json", "r", encoding="utf-8") as file:
        crimes = json.load(file)
except FileNotFoundError:
    print("Error: crimes_bristol.json not found! Please run your fetch script first.")
    exit()

cleaned = []

for crime in crimes:
    location = crime.get("location")
    if not location:
        continue

    lat = location.get("latitude")
    lng = location.get("longitude")
    if not lat or not lng:
        continue

    street = location.get("street", {}).get("name", "Unknown")

    cleaned.append({
        "category": crime["category"],
        "street": street,
        "lat": float(lat),
        "lng": float(lng),
        "month": crime.get("month", "2026-03")
    })

with open("cleaned_crimes_bristol.json", "w", encoding="utf-8") as file:
    json.dump(cleaned, file, indent=2, ensure_ascii=False)

print(f"Success: Cleaned records count: {len(cleaned)}")