# 🗺️ Geospatial Crime Analysis & Risk Mapping System (Bristol, UK)

An advanced, end-to-end Python data pipeline that extracts, processes, and visualizes localized crime data within Bristol and its surroundings. The project leverages mathematical grid-mapping algorithms to overcome API query boundaries, implements an algorithmic risk-scoring system based on custom weights, and renders interactive spatial charts.

---

## 🚀 Key Features

* **Custom Grid-Based Extraction:** Employs a multi-point circular coordinate grid system to completely bypass pagination and size limitations of the official UK Police REST API.
* **Algorithmic Risk Scoring Model:** Groups records by unique geographic locations and weights them analytically based on crime severity thresholds (High, Medium, Low risk).
* **Interactive Data Visualization:** Generates responsive point-cluster maps and high-density Heatmaps with dynamic HTML sidebars highlighting top-priority risk spots.
* **Modular Clean-Code Architecture:** The ecosystem is split cleanly into dedicated production-ready layers: Fetching, Cleaning, Processing, and Visualizing.

---

## 🛠️ Project Architecture & Pipeline

Run the scripts sequentially in the following order to construct the database and generate the interactive visual outputs:

### 1. `fetch_brimes_bristol.py`
Calculates a circular matrix grid over a 12 km radius focused on Bristol city center (`51.4545, -2.5879`). It automates HTTP request sequences for the **March 2026** (`2026-03`) period, ignores redundant overlaps, and saves raw outputs to `crimes_bristol.json`.

### 2. `clean_crimes.py`
Parses raw data payloads, drops anomalies lacking strict geographical coordinate parameters (`latitude`/`longitude`), and exports normalized records to `cleaned_crimes_bristol.json`.

### 3. `process_crimes.py`
Applies a tailored severity matrix (e.g., *Violent Crime: 7*, *Robbery: 6*, *Burglary: 5*, *Shoplifting: 1*) to map and calculate aggregated hazard scores for unique streets. It evaluates dynamic risk boundaries and saves structured results to `risk_bristol.json`.

### 4. Visualizations (`create_map.py` & `bristol_crime_heatmap.py`)
Generates rich geospatial charts integrating automated screen-bounding (`fit_bounds`) to ensure all analyzed grid locations are perfectly framed upon load.
* `create_map.py` -> Outputs a pinpoint marker layout: `bristol_crime_map.html`.
* `bristol_crime_heatmap.py` -> Outputs a cluster heat graph with a responsive top-10 risk dashboard overlay: `bristol_crime_heatmap.html`.

---

## 🗂️ Tech Stack & Dependencies

* **Language:** Python 3.x
* **Core Libraries:** `requests`, `folium`, `json`, `math`, `time`, `collections`
* **Data Provider:** Official UK Police REST API (`data.police.uk`)

---

## 📊 Live Interactive Previews

GitHub does not render raw interactive HTML templates by default. You can seamlessly experience the dynamic features of the generated analytical maps by using the secure mirrors below:

🔗 **[Click Here to Open the Interactive Point-Cluster Map](https://htmlpreview.github.io/?https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME/blob/main/bristol_crime_map.html)**

🔗 **[Click Here to Open the Live Dynamic Crime Heatmap](https://htmlpreview.github.io/?https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME/blob/main/bristol_crime_heatmap.html)**

*(Note: Please replace `YOUR_GITHUB_USERNAME` and `YOUR_REPO_NAME` in the links above with your actual GitHub username and repository name after publishing.)*

---

## 👥 Contributors

This system was conceptualized, architected, and developed collaboratively by:
* **Arda Yalın Uçar** 
* **Mehmet Olgun**