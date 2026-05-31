import json
import folium

try:
    with open("risk_bristol.json", "r", encoding="utf-8") as file:
        results = json.load(file)
except FileNotFoundError:
    print("Error: risk_bristol.json not found! Please run process_crimes.py first.")
    exit()

try:
    with open("cleaned_crimes_bristol.json", "r", encoding="utf-8") as file:
        raw_crimes = json.load(file)
        crime_month = raw_crimes[0].get("month", "2026-03")
except Exception:
    crime_month = "2026-03"

print(f"📊 Analyzed Period: {crime_month}")


bristol_map = folium.Map(location=[51.4545, -2.5879], zoom_start=11)
all_coordinates = []

for item in results:
    lat = item["lat"]
    lng = item["lng"]
    street = item["street"]
    score = item["risk_score"]
    level = item["risk_level"]

    all_coordinates.append([lat, lng])

    if level == "high":
        color = "red"
    elif level == "medium":
        color = "orange"
    else:
        color = "green"

    popup_text = f"""
    <b>Street:</b> {street}<br>
    <b>Risk Score:</b> {score}<br>
    <b>Risk Level:</b> {level.upper()}<br>
    <b>Period:</b> {crime_month}
    """

    folium.CircleMarker(
        location=[lat, lng],
        radius=6,
        popup=folium.Popup(popup_text, max_width=300),
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.8
    ).add_to(bristol_map)


if all_coordinates:
    bristol_map.fit_bounds(all_coordinates)

output_filename = "bristol_crime_map.html"
bristol_map.save(output_filename)

print(f"🎉 Your customized Bristol crime map is ready as '{output_filename}'!")