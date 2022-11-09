using Microsoft.MixedReality.Toolkit.Utilities;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Axis : MonoBehaviour
{
    public Microsoft.MixedReality.Toolkit.Utilities.AxisFlags axis;
    private AxisManager axisManager;
    private AlignmentManager alignmentManager;
    private MeshRenderer grabHighlightMesh;

    private void Awake()
    {
        axisManager = transform.parent.GetComponent<AxisManager>();
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

    /*

    public void Activate()
    {
        AxisFlags flag = ~axis;
        alignmentManager.SetNudgeAxis(flag);
        grabHighlightMesh.enabled = true;
    }

    public void Deactivate()
    {
        //alignmentManager.SetNudgeAxis(axis);
        grabHighlightMesh.enabled = false;
    }
    */

    public void SetVisibility(bool visibile)
    {
        grabHighlightMesh.enabled = visibile;
    }

    public void AlertManager()
    {
        axisManager.ActivateAxis(this, axis);
    }

}
