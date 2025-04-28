import json
import pandas as pd
from google.colab import files

# Step 1: Specify the JSON file path
file_path = "/content/interlink-metrics-default-rtdb-export-2.json"

# Step 2: Load the JSON data
with open(file_path, "r") as file:
    all_sessions = json.load(file)

# Step 3: Define target levels and waves
target_levels = ["Beta-Cavern", "Beta-Vines"]
wave_names = ["Wave 1", "Wave 2", "Wave 3", "Wave 4"]

# Step 4: Extract rope connection/disconnection metrics
metrics = []

for session_id, session_data in all_sessions.items():
    for level_data in session_data.get("m_levelMetricsData", []):
        level_name = level_data.get("m_levelName")
        if level_name in target_levels:
            connections = level_data.get("m_ropeConnectionMetrics", [])
            disconnections = level_data.get("m_ropeDisconnectionMetrics", [])

            if len(connections) == len(disconnections) == 4:
                for wave_index in range(4):
                    metrics.append({
                        "Session": session_id,
                        "Level": level_name,
                        "Wave": wave_names[wave_index],
                        "Rope Connections": connections[wave_index],
                        "Rope Disconnections": disconnections[wave_index]
                    })

# Step 5: Create a DataFrame and save to CSV
df = pd.DataFrame(metrics)
output_file = "/content/rope_metrics_beta_levels.csv"
df.to_csv(output_file, index=False)
files.download(output_file)

# Step 6: Optional preview
df.head()