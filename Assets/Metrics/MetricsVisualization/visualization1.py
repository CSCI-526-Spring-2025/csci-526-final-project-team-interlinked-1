import json
import pandas as pd

# Load the JSON file
file_path = "/content/interlink-metrics-default-rtdb-export-2.json"
with open(file_path, "r") as file:
    all_sessions = json.load(file)

rope_detailed_data = []

for session_id, session_data in all_sessions.items():
    for level in session_data.get("m_levelMetricsData", []):
        level_name = level.get("m_levelName")
        conn_list = level.get("m_ropeConnectionMetrics", [])
        disc_list = level.get("m_ropeDisconnectionMetrics", [])

        rope_detailed_data.append({
            "session_id": session_id,
            "level_name": level_name,
            "rope_connections": sum(conn_list),
            "rope_disconnections": sum(disc_list)
        })

# Rebuild rope DataFrame
rope_detailed_df = pd.DataFrame(rope_detailed_data)
rope_detailed_df.to_csv("/content/rope_connections_disconnections_boxplot.csv", index=False)

# For weapon steal rates and abilities, attach level name to each entry
weapon_level_data_detailed = []
ability_data_detailed = []

for session_id, session_data in all_sessions.items():
    level_names = [lvl.get("m_levelName") for lvl in session_data.get("m_levelMetricsData", [])]

    # Assign to all known levels for this session
    for weapon in session_data.get("m_weaponMetricsData", []):
        for level_name in level_names:
            weapon_level_data_detailed.append({
                "session_id": session_id,
                "level_name": level_name,
                "weapon_name": weapon.get("m_weaponName"),
                "steal_rate": weapon.get("m_stealRate")
            })

    for ability in session_data.get("m_abilityMetricsData", []):
        for level_name in level_names:
            ability_data_detailed.append({
                "session_id": session_id,
                "level_name": level_name,
                "ability_name": ability.get("m_abilityName"),
                "activation_rate": ability.get("m_activationRate")
            })

# Create detailed DataFrames
weapon_level_df_detailed = pd.DataFrame(weapon_level_data_detailed)
ability_df_detailed = pd.DataFrame(ability_data_detailed)

# Save to CSV
weapon_level_df_detailed.to_csv("/content/weapon_steal_rate_by_level_boxplot.csv", index=False)
ability_df_detailed.to_csv("/content/special_ability_activation_rate_by_level_boxplot.csv", index=False)