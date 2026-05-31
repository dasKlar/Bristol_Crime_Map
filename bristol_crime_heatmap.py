import json
import folium
from folium.plugins import HeatMap


try:
    with open("risk_bristol.json", "r", encoding="utf-8") as file:
        results = json.load(file)
except FileNotFoundError:
    print("Error: risk_bristol.json not found! Please run process_crimes.py first.")
    exit()


top_locations = results[:10]


bristol_map = folium.Map(location=[51.4545, -2.5879], zoom_start=11)


sidebar_html = """
<div style="
position: fixed;
top: 15px;
right: 15px;
width: 260px;
height: 300px;
overflow-y: auto;
background-color: white;
border: 1px solid #999;
z-index:9999;
padding: 10px;
font-size: 12px;
font-family: Arial, sans-serif;
box-shadow: 2px 2px 8px rgba(0,0,0,0.25);
border-radius: 8px;
">
<h4 style="margin-top:0;">🔴 Top Risk Locations</h4>
"""

for index, item in enumerate(top_locations, start=1):
    crime_types = item.get("crime_types", {})
    most_common_crime = max(crime_types, key=crime_types.get) if crime_types else "N/A"

    sidebar_html += f"""
    <div style="margin-bottom:8px;">
        <b>{index}. {item['street']}</b><br>
        <span>Risk Score: {item['risk_score']}</span><br>
        <span>Reports: {item['total_crimes']}</span><br>
        <span>Main Issue: {most_common_crime}</span>
    </div>
    <hr style="border:0; border-top:1px solid #eee;">
    """

sidebar_html += "</div>"


heatmap_layer = folium.FeatureGroup(name="Heatmap")
high_risk_layer = folium.FeatureGroup(name="High Risk Locations")


heat_data = [
    [item["lat"], item["lng"], item["risk_score"]]
    for item in results
]

HeatMap(
    heat_data,
    radius=18,
    blur=15,
    max_zoom=13
).add_to(heatmap_layer)


all_coordinates = []


for item in results:
    lat = item["lat"]
    lng = item["lng"]
    street = item["street"]
    score = item["risk_score"]
    level = item["risk_level"]

    all_coordinates.append([lat, lng])


    if level != "high":
        continue

    color = "red"
    total_crimes = item["total_crimes"]
    crime_types = item["crime_types"]

    most_common_crime = max(crime_types, key=crime_types.get) if crime_types else "N/A"
    most_common_count = crime_types[most_common_crime] if crime_types else 0

    recommendation = "Stay alert and avoid displaying valuables in this area."

    popup_text = f"""
    <div style="font-family: Arial; width: 230px;">
         <h3 style="margin-bottom: 6px;">📍 {street}</h3>
         <p><b style="color:red;">🔴 HIGH RISK</b></p>
         <p><b>Risk Score:</b> {score}</p>
         <p><b>Total Crimes:</b> {total_crimes}</p>
         <p><b>Most Common Crime:</b><br>{most_common_crime} ({most_common_count})</p>
         <hr>
         <p><b>Recommendation:</b><br>{recommendation}</p>
    </div>
    """

    folium.CircleMarker(
        location=[lat, lng],
        radius=max(5, min(score / 20, 15)),
        popup=folium.Popup(popup_text, max_width=300),
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(high_risk_layer)


heatmap_layer.add_to(bristol_map)
high_risk_layer.add_to(bristol_map)

bristol_map.get_root().html.add_child(
    folium.Element(sidebar_html)
)

folium.LayerControl(position="bottomleft").add_to(bristol_map)


if all_coordinates:
    bristol_map.fit_bounds(all_coordinates)


output_filename = "bristol_crime_heatmap.html"
bristol_map.save(output_filename)

print(f"🎉 Your dynamic Bristol crime heatmap is ready as '{output_filename}'!")