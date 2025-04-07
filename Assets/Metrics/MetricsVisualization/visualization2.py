import json
import pandas as pd
from google.colab import files

# STEP 1: Upload your JSON file (e.g. interlink-metrics-default-rtdb-export-2.json)
filename = "/content/interlink-metrics-default-rtdb-export-2.json"

# STEP 2: Load and parse the JSON
with open(filename, 'r') as f:
    data = json.load(f)

# STEP 3: Extract metrics for Beta-Cavern and Beta-Vines
levels_of_interest = ["Beta-Cavern", "Beta-Vines"]
wave_labels = ["Wave 1", "Wave 2", "Wave 3", "Wave 4"]

records = []

for session_id, session in data.items():
    level_metrics = session.get("m_levelMetricsData", [])
    for level in level_metrics:
        level_name = level.get("m_levelName")
        if level_name in levels_of_interest:
            conn = level.get("m_ropeConnectionMetrics", [])
            disc = level.get("m_ropeDisconnectionMetrics", [])
            if conn and disc and len(conn) == 4 and len(disc) == 4:
                for i in range(4):
                    records.append({
                        "Session": session_id,
                        "Level": level_name,
                        "Wave": wave_labels[i],
                        "Rope Connections": conn[i],
                        "Rope Disconnections": disc[i]
                    })

# STEP 4: Convert to DataFrame and save to CSV
df = pd.DataFrame(records)
csv_filename = "/content/rope_metrics_beta_levels.csv"
df.to_csv(csv_filename, index=False)
files.download(csv_filename)

# Optional Preview
df.head()