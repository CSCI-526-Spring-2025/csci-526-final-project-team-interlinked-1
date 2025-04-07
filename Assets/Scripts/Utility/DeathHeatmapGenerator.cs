using System.Collections.Generic;
using UnityEngine;

[ExecuteInEditMode]
public class DeathHeatmapGenerator : MonoBehaviour
{
    [Header("Grid Settings")]
    public Vector2 gridOrigin = new Vector2(-50, -50);  // Bottom-left of the level
    public Vector2 gridSize = new Vector2(100, 100);    // Width & height of the level
    public float cellSize = 5f;                         // Size of each block

    [Header("Data Input")]
    public TextAsset jsonFile;                          // Paste Firebase JSON here

    private int[,] heatmapGrid;
    private int rows, cols;

    [System.Serializable]
    public class DeathPosition
    {
        public float x;
        public float y;
    }

    [System.Serializable]
    public class LevelData
    {
        public string m_levelName;
        public int m_deathCount;
        public List<DeathPosition> m_deathLocations;
    }

    [System.Serializable]
    public class SessionData
    {
        public string m_sessionID;
        public List<LevelData> m_levelMetricsData;
    }

    [System.Serializable]
    private class Wrapper
    {
        public Dictionary<string, SessionData> root;
    }

    void Start()
    {
        LoadHeatmapData();
    }

    void LoadHeatmapData()
    {
        rows = Mathf.CeilToInt(gridSize.y / cellSize);
        cols = Mathf.CeilToInt(gridSize.x / cellSize);
        heatmapGrid = new int[cols, rows];

        if (jsonFile == null)
        {
            Debug.LogWarning("No JSON file assigned.");
            return;
        }

        string wrappedJson = "{\"root\":" + jsonFile.text + "}";
        Wrapper wrapper = JsonUtility.FromJson<Wrapper>(wrappedJson);

        foreach (var session in wrapper.root.Values)
        {
            foreach (var level in session.m_levelMetricsData)
            {
                foreach (var death in level.m_deathLocations)
                {
                    int col = Mathf.FloorToInt((death.x - gridOrigin.x) / cellSize);
                    int row = Mathf.FloorToInt((death.y - gridOrigin.y) / cellSize);

                    if (col >= 0 && col < cols && row >= 0 && row < rows)
                    {
                        heatmapGrid[col, row]++;
                    }
                }
            }
        }
    }

    void OnDrawGizmos()
    {
        if (heatmapGrid == null) return;

        int maxDeaths = 1;
        foreach (int count in heatmapGrid)
        {
            if (count > maxDeaths) maxDeaths = count;
        }

        for (int x = 0; x < cols; x++)
        {
            for (int y = 0; y < rows; y++)
            {
                int deathCount = heatmapGrid[x, y];
                if (deathCount > 0)
                {
                    float alpha = (float)deathCount / maxDeaths;
                    Color color = new Color(1f, 0f, 0f, alpha); // red with intensity
                    Gizmos.color = color;

                    Vector3 center = new Vector3(
                        gridOrigin.x + x * cellSize + cellSize / 2,
                        gridOrigin.y + y * cellSize + cellSize / 2,
                        0f
                    );

                    Gizmos.DrawCube(center, new Vector3(cellSize, cellSize, 0.1f));
                }
            }
        }
    }
}