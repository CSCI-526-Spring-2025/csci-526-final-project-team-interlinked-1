using UnityEngine;
using DG.Tweening;

public class MoveAlongPath : MonoBehaviour
{
    // Define the path (array of Vector3 points)
    public Vector3[] path;

    // Duration to complete the path movement
    public float duration = 3f;

    void Start()
    {
        // Set up the path points, you can manually set these in the Inspector or define them here.
        path = new Vector3[]
        {
            new Vector3(0, 0, 0), // Starting point
            new Vector3(5, 5, 0), // First curve point
            new Vector3(10, 0, 0), // Second curve point
            new Vector3(15, 5, 0)  // End point
        };

        // Animate the GameObject along the path using DOPath
        AnimateAlongPath();
    }

    void AnimateAlongPath()
    {
        // Move the GameObject along the defined path
        transform.DOPath(path, duration, PathType.CatmullRom)  // Use CatmullRom for smooth curve
            .SetEase(Ease.Linear)  // Optional, to control the ease of the movement (you can change this)
            .OnComplete(() => Debug.Log("Path animation completed!")); // Optional completion callback
    }
}
