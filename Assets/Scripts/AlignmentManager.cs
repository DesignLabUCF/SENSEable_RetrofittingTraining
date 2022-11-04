using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;
using Microsoft.MixedReality.SENSEableQR;
using Microsoft.MixedReality.WorldLocking.Core;
using static Microsoft.MixedReality.WorldLocking.Core.SpacePin;

public class AlignmentManager : MonoBehaviour
{
    public BIMManager bimManager;
    public bool scanningActive = true;
    //public bool structureVisible = false;
    public int DesiredScans = 100;
    public List<Vector3> scanPositions;
    public List<Vector3> scanRotations; // Euler angles
    public List<float> scanSizes; // QR size
    private TextMeshPro text;
    private float xRotationOffset = 180.0f; // In degrees; Formerly 180f
    private string anchorName = "SENSEableRetrofittingAnchor";
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
    }

    // Update is called once per frame
    void Update()
    {

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
            // Check for outlier
            /// TODO
            // Collect
            scanPositions.Add(scanPosition);
            scanRotations.Add(scanRotation);
            scanSizes.Add(QRSize);
            // Check if we are done scanning for QR codes
            if(scanPositions.Count >= DesiredScans)
            {
                ScanningComplete();
            }
            // Update count text
            SetText(scanPositions.Count, DesiredScans);
            // Update average preview
            transform.position = GetAveragePosition();
            transform.eulerAngles = GetAverageRotation();
            // Lock world Position
            /// TODO
        }
    }

    private void ScanningComplete()
    {
        scanningActive = false;
        text.gameObject.SetActive(false);
        SetQRIndicatorVisibility(false);
        GameObject.FindObjectOfType<DataLogger>().LogAlignmentComplete();
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
        transform.position = Vector3.zero;
        transform.eulerAngles = Vector3.zero;
        scanningActive = true;
        bimManager.SetVisibility(false);
        text.gameObject.SetActive(true);
        SetText(scanPositions.Count, DesiredScans);
        SetQRIndicatorVisibility(true);
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

    //private void SetStructureVisbility(bool visibility)
    //{
    //    scanObjectRoot.SetActive(visibility);
    //    structureVisible = visibility;
    //}
}
