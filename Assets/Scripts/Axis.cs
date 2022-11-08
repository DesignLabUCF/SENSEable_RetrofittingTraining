using Microsoft.MixedReality.Toolkit.Utilities;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Axis : MonoBehaviour
{
    public Microsoft.MixedReality.Toolkit.Utilities.AxisFlags axis;
    private AlignmentManager alignmentManager;
    private MeshRenderer grabHighlightMesh;

    private void Awake()
    {
        alignmentManager = GameObject.FindObjectOfType<AlignmentManager>();
        grabHighlightMesh = transform.Find("GrabHighlight").GetComponent<MeshRenderer>();
    }

    // Start is called before the first frame update
    void Start()
    {
        grabHighlightMesh.enabled = false;
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    /*
    public void SetAxisOnManager()
    {
        alignmentManager.SetNudgeAxis(axis);
    }

    private void OnCollisionEnter(Collision collision)
    {
        SetAxisOnManager();
    }
    */

    public void ActivateAxis()
    {
        AxisFlags flag = ~axis;
        alignmentManager.SetNudgeAxis(flag);
        grabHighlightMesh.enabled = true;
    }

    public void DeactivateAxis()
    {
        //alignmentManager.SetNudgeAxis(axis);
        grabHighlightMesh.enabled = false;
    }
}
