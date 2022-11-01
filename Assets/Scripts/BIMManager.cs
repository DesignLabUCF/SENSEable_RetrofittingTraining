using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BIMManager : MonoBehaviour
{
    public GameObject rootObject;
    public bool isVisible = false;

    // Start is called before the first frame update
    void Start()
    {
        if(rootObject == null)
            Debug.LogError("Root BIM object not set.");
        SetVisibility(false);
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void SetVisibility(bool visibility)
    {
        isVisible = visibility;
        rootObject.SetActive(isVisible);
    }
}
