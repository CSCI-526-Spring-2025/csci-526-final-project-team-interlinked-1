import json
import pandas as pd

# Load the JSON file
file_path = "/content/interlink-metrics-default-rtdb-export-2.json"
with open(file_path, "r") as file:
    all_sessions = json.load(file)

# Process rope connection and disconnection metrics
rope_metrics = []

for session_id, session_data in all_sessions.items():
    for level in session_data.get("m_levelMetricsData", []):
        rope_metrics.append({
            "session_id": session_id,
            "level_name": level.get("m_levelName"),
            "rope_connections": sum(level.get("m_ropeConnectionMetrics", [])),
            "rope_disconnections": sum(level.get("m_ropeDisconnectionMetrics", []))
        })

# Create and save rope metrics DataFrame
rope_df = pd.DataFrame(rope_metrics)
rope_df.to_csv("/content/rope_connections_disconnections_boxplot.csv", index=False)

# Process weapon steal rates and ability activation rates
weapon_data = []
ability_data = []

for session_id, session_data in all_sessions.items():
    level_names = [level.get("m_levelName") for level in session_data.get("m_levelMetricsData", [])]

    for weapon in session_data.get("m_weaponMetricsData", []):
        for level_name in level_names:
            weapon_data.append({
                "session_id": session_id,
                "level_name": level_name,
                "weapon_name": weapon.get("m_weaponName"),
                "steal_rate": weapon.get("m_stealRate")
            })

    for ability in session_data.get("m_abilityMetricsData", []):
        for level_name in level_names:
            ability_data.append({
                "session_id": session_id,
                "level_name": level_name,
                "ability_name": ability.get("m_abilityName"),
                "activation_rate": ability.get("m_activationRate")
            })

# Create and save weapon and ability metrics DataFrames
weapon_df = pd.DataFrame(weapon_data)
ability_df = pd.DataFrame(ability_data)

weapon_df.to_csv("/content/weapon_steal_rate_by_level_boxplot.csv", index=False)
ability_df.to_csv("/content/special_ability_activation_rate_by_level_boxplot.csv", index=False)