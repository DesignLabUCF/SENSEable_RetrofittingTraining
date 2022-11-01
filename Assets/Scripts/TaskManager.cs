using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TaskManager : MonoBehaviour
{
    private int currentTaskIndex = 0;
    public Task currentTask = null;
    public List<Task> taskList;
    public TaskMenu taskMenu;

    // Start is called before the first frame update
    void Start()
    {
        for(int i = 0; i < transform.childCount; i++)
            taskList.Add(transform.GetChild(i).GetComponent<Task>());

        currentTaskIndex = 0;
        LoadTask(0);
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void LoadTask(int taskIndex)
    {
        currentTaskIndex = taskIndex;
        currentTask = taskList[currentTaskIndex];
        // Hide all holograms on all tasks
        for(int i = 0; i < taskList.Count; i++)
        {
            taskList[i].SetHologramsVisibility(false);
            //SetTaskHologramVisibility(false, taskList[i]);
        }
        // Update GUI
        taskMenu.UpdateGUI(currentTask.taskNumber, currentTask.taskName, currentTask.instructions, currentTask.image);
        // Show holograms for this task
        currentTask.SetHologramsVisibility(true);
        //SetTaskHologramVisibility(true, currentTask);
        // Update data log
        GameObject.FindObjectOfType<DataLogger>().LogTaskStarted(currentTask);
    }

    /*
    private void SetTaskHologramVisibility(bool visibility, Task task)
    {
        int hologramCount = task.gameObject.transform.childCount;
        if(hologramCount == 0)
            return;
        for(int i = 0; i < hologramCount; i++)
            task.gameObject.transform.GetChild(i).gameObject.SetActive(visibility);
    }
    */

    public void NextTask()
    {
        currentTaskIndex = Mathf.Min(currentTaskIndex + 1, taskList.Count - 1);
        LoadTask(currentTaskIndex);
    }

    public void PreviousTask()
    {
        currentTaskIndex = Mathf.Max(currentTaskIndex - 1, 0);
        LoadTask(currentTaskIndex);
    }
}
