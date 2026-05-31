import requests
import json
import time
import math
from collections import Counter

url = "https://data.police.uk/api/crimes-street/all-crime"
target_date = "2026-03"

center_lat = 51.4545
center_lng = -2.5879
max_radius_km = 12.0


grid_points = []
step_km = 2.2

lat_degree_km = 111.0
lng_degree_km = 111.0 * math.cos(math.radians(center_lat))

search_range = int(max_radius_km / step_km) + 1

for i in range(-search_range, search_range + 1):
    for j in range(-search_range, search_range + 1):
        delta_lat = i * step_km
        delta_lng = j * step_km
        distance = math.sqrt(delta_lat ** 2 + delta_lng ** 2)


        if distance <= max_radius_km:
            pt_lat = center_lat + (delta_lat / lat_degree_km)
            pt_lng = center_lng + (delta_lng / lng_degree_km)
            grid_points.append((round(pt_lat, 4), round(pt_lng, 4)))

all_crimes_dict = {}

print(f"🌍 Starting BRISTOL circular area analysis for period: {target_date}")
print(f"🎯 Scanning {len(grid_points)} micro-regions to assemble the main boundary.\n")

# Step 3: Send API requests for the Bristol grid system
for index, (lat, lng) in enumerate(grid_points, start=1):
    print(f"⏳ [{index}/{len(grid_points)}] Scanning coordinates: {lat}, {lng}...")

    payload = {
        "date": target_date,
        "lat": str(lat),
        "lng": str(lng)
    }

    for attempt in range(3):
        try:
            response = requests.get(url, params=payload, timeout=20)
            if response.status_code == 200:
                sector_crimes = response.json()

                for crime in sector_crimes:
                    crime_id = crime.get("id")
                    if crime_id:
                        all_crimes_dict[crime_id] = crime
                break
            elif response.status_code == 503:
                time.sleep(2)
            else:
                break
        except Exception:
            time.sleep(2)

    time.sleep(0.2)

all_crimes = list(all_crimes_dict.values())

with open("crimes_bristol.json", "w", encoding="utf-8") as file:
    json.dump(all_crimes, file, indent=2, ensure_ascii=False)

category_counts = Counter(crime["category"] for crime in all_crimes)

print("\n" + "=" * 50)
print(f"🎉 PROCESS COMPLETED! Total unique crime records found in Bristol: {len(all_crimes)}")
print("=" * 50)
print("\nCrime Distribution in Bristol:")
for category, count in category_counts.most_common():
    print(f"- {category}: {count}")

print("\n👉 Bristol data has been successfully saved to 'crimes_bristol.json'.")