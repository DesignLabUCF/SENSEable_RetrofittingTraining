using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CubeManager : MonoBehaviour
{
    private List<GameObject> cubes;
    public GameObject cube1;
    public GameObject cube2;

    // Start is called before the first frame update
    void Start()
    {
        if(cube1 == null || cube2 == null)
        {
            Debug.LogError("CubeManager cubes not set.");
        }

        cubes = new List<GameObject>();
        cubes.Add(cube1);
        cubes.Add(cube2);
    }

    // Update is called once per frame
    void Update()
    {
        /*
        if(Input.GetKeyDown(KeyCode.L))
        {
            ToggleVis();
        }
        */
    }

    public void ToggleVis()
    {
        for(int i = 0; i < cubes.Count; i++)
        {
            cubes[i].SetActive(!cubes[i].activeSelf);
        }
    }
}
