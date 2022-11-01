using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Task : MonoBehaviour
{
    public List<GameObject> holograms;
    public string taskNumber;
    public string taskName;
    public string instructions;
    public Texture image;

    private GameObject hologramsRoot;

    private void Awake()
    {
        hologramsRoot = transform.GetChild(0).gameObject;
    }

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void SetHologramsVisibility(bool visible)
    {
        int hologramCount = hologramsRoot.transform.childCount;
        if(hologramCount == 0)
            return;
        for(int i = 0; i < hologramCount; i++)
            hologramsRoot.transform.GetChild(i).gameObject.SetActive(visible);
    }
}
