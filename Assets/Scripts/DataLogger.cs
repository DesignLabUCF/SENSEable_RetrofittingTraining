using Microsoft.MixedReality.Toolkit;
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Text;
using TMPro;
using UnityEngine;

public class DataLogger : MonoBehaviour
{
    public Camera userCamera;
    public AlignmentManager alignmentManager;
    public TaskMenu taskMenu;
    public TextMeshPro writeProgressText;
    public float interval = 0.25f; // Every 'interval' seconds
    private DateTime previousTime;
    private bool writingToFile = false;
    //private StringBuilder log;
    private List<String> log;
    private string format = "F3";

    private void Awake()
    {
        //log = new StringBuilder();
        log = new List<String>();
    }

    // Start is called before the first frame update
    void Start()
    {
        previousTime = DateTime.Now;
    }

    // Update is called once per frame
    void Update()
    {
        if(HeadDataIsReadyToLog())
        {
            // Read in Gaze data
            bool gazeValid = false;
            Vector3 gazeOrigin = Vector3.zero;
            Vector3 gazeDirection = Vector3.zero;
            if(CoreServices.InputSystem.EyeGazeProvider.IsEyeTrackingEnabled)
            {
                Debug.Log("Eye tracking enabled.");
                if(CoreServices.InputSystem.EyeGazeProvider.IsEyeTrackingDataValid)
                {
                    Debug.Log("Eye tracking is valid.");
                    gazeValid = true;
                    gazeOrigin = CoreServices.InputSystem.EyeGazeProvider.GazeOrigin;
                    gazeDirection = CoreServices.InputSystem.EyeGazeProvider.GazeDirection;
                }
                else
                {
                    Debug.Log("Eye tracking is NOT valid.");
                }
            }
            // Log
            LogHeadData(userCamera.transform, gazeOrigin, gazeDirection, gazeValid, alignmentManager.transform, taskMenu.transform, taskMenu.pinned, taskMenu.visible);
            // Update timestamp
            previousTime = DateTime.Now;
        }
    }

    private bool HeadDataIsReadyToLog()
    {
        TimeSpan diff = DateTime.Now - previousTime;
        float duration = diff.Milliseconds / 1000.0f;
        if(duration >= interval)
            return true;
        else
            return false;
    }

    public void LogHeadData(Transform head, Vector3 gazeOrigin, Vector3 gazeDirection, bool? gazeValid, Transform wall, Transform menu, bool menuPinned, bool menuVisible)
    {
        string data = DataHeader("Head", false) +
            "\n\nHead_Position:\n" +
            head.position.ToString(format) +
            "\n\nHead_Rotation:\n" +
            head.eulerAngles.ToString(format) +
            "\n\nWall_Position:\n" +
            wall.position.ToString(format) +
            "\n\nWall_Rotation:\n" +
            wall.eulerAngles.ToString(format) +
            "\n\nGaze_Valid:\n" +
            gazeValid +
            "\n\nGaze_Origin:\n" +
            gazeOrigin.ToString(format) +
            "\n\nGaze_Direction:\n" +
            gazeDirection.ToString(format) +
            "\n\nMenu_Pinned:\n" +
            menuPinned +
            "\n\nMenu_Position:\n" +
            menu.position.ToString(format) +
            "\n\nMenu_Rotation:\n" +
            menu.rotation.ToString(format) +
            "\n\nMenu_Visible:\n" +
            menuVisible +
            DataFooter();
        AddData(data);
        //log.Add(data);
        //log.Append(data);
        //Debug.Log(data);
    }

    public void LogAlignmentComplete()
    {
        string data = DataHeader("Scan_Complete", true);
        AddData(data);
        //log.Add(data);
        //log.Append(data);
        //Debug.Log(data);
    }

    public void LogTaskStarted(Task task)
    {
        string data = DataHeader("Task_Started", false) +
            "\n\nTask_Name:\n" +
            task.taskName +
            "\n\nTask_Number:\n" +
            task.taskNumber +
            DataFooter();
        AddData(data);
        //log.Add(data);
        //log.Append(data);
        //Debug.Log(data);
    }

    public void LogSetMenuPin(bool pinned)
    {
        string data = DataHeader("Menu_Pin", false) +
            "\n\nMenu_Pinned:\n" +
            pinned +
            DataFooter();
        AddData(data);
        //log.Add(data);
        //log.Append(data);
        //Debug.Log(data);
    }
    private void AddData(string data)
    {
        if(!writingToFile) // Only update GUI text when writing to file is not occuring
            UpdateWriteProgressText(0, log.Count);
        log.Add(data);
    }

    private String DataHeader(string type, bool useEndTerminator)
    {
        string term = "";
        if(useEndTerminator)
            term = "====================\n";
        else
            term = "--------------------\n";

        return "\n====================\n" + type + "\n\nCurrent:\n" + GetTimeSinceLaunch() + "\n\nTimestamp:\n" + GetTimestamp().ToString("MM-dd-yyyy_HH-mm-ss-fff") + "\n\n" + term;
    }

    private String DataFooter()
    {
        return "\n====================\n";
    }

    public void WriteToFile()
    {
        // Create directory if does not exist
        if(!Directory.Exists(Application.persistentDataPath + "/OutputData"))
            Directory.CreateDirectory(Application.persistentDataPath + "/OutputData");
        /*
        // Create and write to the file
        string path = Application.persistentDataPath + "/OutputData/" + GetTimestamp().ToString("MM-dd-yyyy_HH-mm-ss") + ".txt";
        Debug.Log("Writing to file: " + path);
        StreamWriter writer = new StreamWriter(path, true);
        for(int i = 0; i < log.Count; i++)
        {
            writer.Write(log[i]);
        }
        writer.Close();
        */
        // Launch coroutine to run in the background
        StartCoroutine(Save());
    }

    IEnumerator Save()
    {
        writingToFile = true;
        int cutoffIndex = log.Count;
        // Create and write to the file
        string path = Application.persistentDataPath + "/OutputData/" + GetTimestamp().ToString("MM-dd-yyyy_HH-mm-ss") + ".txt";
        Debug.Log("Writing to file: " + path);
        StreamWriter writer = new StreamWriter(path, true);
        for(int i = 0; i < cutoffIndex; i++)
        {
            // Write to file
            writer.Write(log[i]);
            // Update gui
            UpdateWriteProgressText(i + 1, cutoffIndex);
            // Wait till next frame
            yield return null;
        }
        writer.Close();
        writingToFile = false;
    }

    private DateTime GetTimestamp()
    {
        return DateTime.Now;
    }

    private float GetTimeSinceLaunch()
    {
        return Time.realtimeSinceStartup;
    }

    private void UpdateWriteProgressText(int progress, int total)
    {
        writeProgressText.text = progress.ToString() + "<br>" + total.ToString(); 
    }
}
