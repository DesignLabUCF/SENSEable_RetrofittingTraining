using Microsoft.MixedReality.Toolkit.Utilities;
using Microsoft.MixedReality.WorldLocking.Core;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using static Unity.IO.LowLevel.Unsafe.AsyncReadManagerMetrics;

public class AxisManager : MonoBehaviour
{
    private AlignmentManager alignmentManager;
    private Axis xAxis;
    private Axis yAxis;
    private Axis zAxis;

    private void Awake()
    {
        alignmentManager = FindObjectOfType<AlignmentManager>();
        xAxis = transform.Find("AxisPointerX").GetComponent<Axis>();
        yAxis = transform.Find("AxisPointerY").GetComponent<Axis>();
        zAxis = transform.Find("AxisPointerZ").GetComponent<Axis>();
    }

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
    }

    public void ActivateAxis(Axis axis, AxisFlags axisFlag)
    {
        // Set MRTK scripts
        AxisFlags inverseFlag = ~axisFlag;
        alignmentManager.SetNudgeAxis(inverseFlag);
        // Update axis visuals (Hide all)
        xAxis.SetVisibility(false);
        yAxis.SetVisibility(false);
        zAxis.SetVisibility(false);
        // Show active axis
        axis.SetVisibility(true);
    }
}
