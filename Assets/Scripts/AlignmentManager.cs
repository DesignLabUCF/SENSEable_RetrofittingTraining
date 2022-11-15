using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;
using Microsoft.MixedReality.SENSEableQR;
using Microsoft.MixedReality.WorldLocking.Core;
using static Microsoft.MixedReality.WorldLocking.Core.SpacePin;
using Microsoft.MixedReality.Toolkit.UI;
using Microsoft.MixedReality.Toolkit.Input;
using System;

public class AlignmentManager : MonoBehaviour
{
    public GameObject lockButton;
    public BoxCollider nudgeCollider;
    //public BoxCollider xCollider;
    //public BoxCollider yCollider;
    //public BoxCollider zCollider;
    public GameObject grabHighlight;
    public GameObject axis;
    public BIMManager bimManager;
    public bool scanningActive = true;
    //public bool structureVisible = false;
    public int DesiredScans = 100;
    public List<Vector3> scanPositions;
    public List<Vector3> scanRotations; // Euler angles
    public List<float> scanSizes; // QR size
    private bool scansTrimmed = false;
    private bool manipulatorGrabbed = false;
    private TextMeshPro text;
    private float xRotationOffset = 180.0f; // In degrees; Formerly 180f
    //private string anchorName = "SENSEableRetrofittingAnchor";
    //private ulong anchorID = ulong.MaxValue;
    //public AnchorId anchorID = (AnchorId)ulong.MaxValue;
    //private IAttachmentPoint attachmentPoint;
    //private Pose lockedPose = Pose.identity;

    public void Awake()
    {
        scanPositions = new List<Vector3>();
        scanRotations = new List<Vector3>();
        scanSizes = new List<float>();

        text = transform.Find("Text_Count").GetComponent<TextMeshPro>();
    }

    // Start is called before the first frame update
    void Start()
    {
        scanningActive = true;
        SetNudgeability(false);

#if UNITY_EDITOR
        Invoke("DebugScanSim", 5.0f); // For debugging in Editor
#endif
    }

    // Update is called once per frame
    void Update()
    {

    }

    private void DebugScanSim()
    {
        Debug.Log("DEBUG SCAN SIMULATION RUNNING");
        for(int i = 0; i < DesiredScans + 50; i++)
        {
            AddScan(Vector3.forward, Vector3.zero, 0.25f);
        }
        transform.eulerAngles = transform.eulerAngles + (new Vector3(180.0f, 0f, 0f));
    }

    /*
    private AnchorId GetAnchorID()
    {
        return ((AnchorId)anchorID);
    }
    */
    /*
    protected virtual void OnLocationUpdate(Pose adjustment)
    {
        lockedPose = adjustment.Multiply(lockedPose);
    }
    */
    public void WorldLockingSave()
    {
        /*
        // Get Pose
        Pose result = Pose.identity;
        result = transform.GetGlobalPose();
        lockedPose = result;
        // If active, remove anchor
        if (anchorID.IsKnown())
            WorldLockingManager.GetInstance().AlignmentManager.RemoveAlignmentAnchor(anchorID);
        // Add the new anchor
        anchorID = WorldLockingManager.GetInstance().AlignmentManager.AddAlignmentAnchor(anchorName, lockedPose, lockedPose);
        // Send
        WorldLockingManager.GetInstance().AlignmentManager.SendAlignmentAnchors();
        if(anchorID.IsKnown())
        {
            IAttachmentPointManager attachmentPointManager = WorldLockingManager.GetInstance().AttachmentPointManager;
            if (attachmentPoint == null)
            {
                attachmentPoint = attachmentPointManager.CreateAttachmentPoint(lockedPose.position, null, OnLocationUpdate, null);
            }
            else
            {
                attachmentPointManager.TeleportAttachmentPoint(attachmentPoint, lockedPose.position, null);
            }
        }
        */
        // Save
        WorldLockingManager.GetInstance().Save();

    }

    public void WorldLockingLoad()
    {
        WorldLockingManager.GetInstance().Load();
    }

    public void AddScan(Vector3 scanPosition, Vector3 scanRotation, float QRSize)
    {
        if(scanningActive == true)
        {
            // Check for faulty scan
            if(scanPosition == Vector3.zero)
                return;
            // Show structure if inital scan
            if(bimManager.isVisible == false)
            {
                bimManager.SetVisibility(true);
            }
            // First few scans sometimes come out wonky, so just re-do them
            if(scansTrimmed == false & scanPositions.Count > 20)
            {
                scansTrimmed = true;
                scanPositions.RemoveRange(0, 5);
                scanRotations.RemoveRange(0, 5);
                scanSizes.RemoveRange(0, 5);
            }
            // Normalize rotation (issues arrise if some are below 0 and become >~350
            scanRotation.x = NormalizeRotation(scanRotation.x);
            scanRotation.y = NormalizeRotation(scanRotation.y);
            scanRotation.z = -NormalizeRotation(scanRotation.z);
            // Collect
            scanPositions.Add(scanPosition);
            scanRotations.Add(scanRotation);
            scanSizes.Add(QRSize);
            // Update count text
            SetText(scanPositions.Count, DesiredScans);
            // Check if we are done scanning for QR codes
            if (scanPositions.Count >= DesiredScans)
            {
                ScanningComplete();
            }
            // Update average preview
            transform.position = GetAveragePosition();
            transform.eulerAngles = GetAverageRotation();
        }
    }

    private void ScanningComplete()
    {
        scanningActive = false;
        text.gameObject.SetActive(false);
        SetQRIndicatorVisibility(false);
        GameObject.FindObjectOfType<DataLogger>().LogAlignmentComplete();
        SetNudgeability(true);
    }

    private void SetNudgeability(bool canNudge)
    {
        axis.SetActive(canNudge);
        if(canNudge)
            axis.GetComponent<AxisManager>().InitialActivation();
        manipulatorGrabbed = false;
        nudgeCollider.enabled = canNudge;
        //xCollider.enabled = canNudge;
        //yCollider.enabled = canNudge;
        //zCollider.enabled = canNudge;
        GetComponent<NearInteractionGrabbable>().enabled = canNudge;
        GetComponent<ObjectManipulator>().enabled = canNudge;
        GetComponent<MinMaxScaleConstraint>().enabled = canNudge;
        GetComponent<MoveAxisConstraint>().enabled = canNudge;
        lockButton.SetActive(canNudge);
    }

    public void NudgeComplete()
    {
        SetGrabHighlightVisibility(false);
        SetNudgeability(false);
        GameObject.FindObjectOfType<DataLogger>().LogWallLocked();
    }

    private float NormalizeRotation(float rot)
    {
        float normalized = rot;
        if(rot <= 45.0f || rot >= (360.0f - 45.0f))
        {
            normalized = normalized - 180.0f;
            if (normalized < 0f)
            {
                normalized = normalized + 180.0f;
            }
            else
            {
                normalized = normalized - 180.0f;
            }
        }
        return normalized;
    }

    private Vector3 GetAveragePosition()
    {
        Vector3 average = Vector3.zero;
        for(int i = 0; i < scanPositions.Count; i++)
        {
            average = average + scanPositions[i];
        }
        return new Vector3(average.x / ((float)scanPositions.Count), average.y / ((float)scanPositions.Count), average.z / ((float)scanPositions.Count));
    }

    private Vector3 GetAverageRotation()
    {
        Vector3 average = Vector3.zero;
        for(int i = 0; i < scanRotations.Count; i++)
        {
            average = average + scanRotations[i];
        }
        return new Vector3(
            (average.x / ((float)scanRotations.Count)) + xRotationOffset,
            average.y / ((float)scanRotations.Count), 
            average.z / ((float)scanRotations.Count));
    }

    private float GetAverageSize()
    {
        float average = 0;
        for(int i = 0; i < scanSizes.Count; i++)
        {
            average = average + scanSizes[i];
        }
        return average / ((float)scanSizes.Count);
    }

    public void ResetScans()
    {
        scanPositions.Clear();
        scanRotations.Clear();
        scansTrimmed = false;
        transform.position = Vector3.zero;
        transform.eulerAngles = Vector3.zero;
        scanningActive = true;
        bimManager.SetVisibility(false);
        text.gameObject.SetActive(true);
        SetText(scanPositions.Count, DesiredScans);
        SetQRIndicatorVisibility(true);
        SetNudgeability(false);
    }

    private void SetText(int n, int max)
    {
        text.text = n.ToString() + " / " + max.ToString();
    }

    private void SetQRIndicatorVisibility(bool visible)
    {
        SENSEableQR[] qrs = FindObjectsOfType<SENSEableQR>();
        // Can't just disable/enable the object, as this causes problems if they're reset and need to be used again.
        foreach(SENSEableQR qr in qrs)
        {
            // So instead, set every descendant's renderer
            foreach(MeshRenderer meshRenderer in qr.gameObject.transform.GetComponentsInChildren<MeshRenderer>())
            {
                meshRenderer.enabled = visible;
            }
        }
    }

    public void NudgeStarted()
    {
        manipulatorGrabbed = true;
    }

    public void NudgeEnded()
    {
        manipulatorGrabbed = false;
    }

    public void SetGrabHighlightVisibility(bool visible)
    {
        grabHighlight.SetActive(visible);
    }

    public void SetNudgeAxis(Microsoft.MixedReality.Toolkit.Utilities.AxisFlags axis)
    {
        Debug.Log("Setting axis: " + axis.ToString());
        if(manipulatorGrabbed == false)
            GetComponent<RotationAxisConstraint>().ConstraintOnRotation = axis;
    }
}
