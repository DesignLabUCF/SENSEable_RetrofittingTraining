using Microsoft.MixedReality.Toolkit.Input;
using Microsoft.MixedReality.Toolkit.UI;
using Microsoft.MixedReality.Toolkit.Utilities.Solvers;
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class TaskMenu : MonoBehaviour
{
    public Interactable handMenuToggle;
    public BIMManager bimManager;
    public Interactable pinToggle;
    public Interactable hologramToggle;
    public GameObject menuContentRoot;
    public bool visible = false;
    public bool pinned = false;
    public TextMeshPro taskNumberMesh;
    public TextMeshPro taskNameMesh;
    public TextMeshPro instructionsMesh;
    public MeshRenderer imageQuadRenderer;

    // Start is called before the first frame update
    void Start()
    {
        if(pinToggle == null)
            Debug.LogError("Pin toggle not set.");
        if(hologramToggle == null)
            Debug.LogError("Pin toggle not set.");
        if(menuContentRoot == null)
            Debug.LogError("MenuConent variable not set.");

        // Set initial menu conditions
        visible = false;
        pinned = false;
        SetPinned();
        SetHologram();
        gameObject.SetActive(false);
    }

    // Update is called once per frame
    void Update()
    {
        
    }


    public void ToggleVisibility()
    {
        SetVisibility(!visible);
    }

    public void SetVisibility(bool newVisibility)
    {
        visible = newVisibility;
        //menuContentRoot.SetActive(visible);
        gameObject.SetActive(visible);
    }

    public void CloseMenu()
    {
        // Update Hand Menu
        handMenuToggle.IsToggled = false;
        // Hide window
        SetVisibility(false);
    }

    public void SetPinned()
    {
        Debug.Log("Setting menu pin status to: " + pinToggle.IsToggled);
        pinned = pinToggle.IsToggled;
        // Pin active
        if(pinToggle.IsToggled == true)
        {
            // Grab-y stuff
            this.GetComponent<NearInteractionGrabbable>().enabled = true;
            this.GetComponent<ObjectManipulator>().enabled = true;
            this.GetComponent<ConstraintManager>().enabled = true;
            this.GetComponent<BoxCollider>().enabled = true;
            // Follow-y stuff
            this.GetComponent<SolverHandler>().enabled = false;
            this.GetComponent<Follow>().enabled = false;
        }
        // Pin inactive
        else
        {
            // Grab-y stuff
            this.GetComponent<NearInteractionGrabbable>().enabled = false;
            this.GetComponent<ObjectManipulator>().enabled = false;
            this.GetComponent<ConstraintManager>().enabled = false;
            this.GetComponent<BoxCollider>().enabled = false;
            // Follow-y stuff
            this.GetComponent<SolverHandler>().enabled = true;
            this.GetComponent<Follow>().enabled = true;
        }
        // Log the change
        GameObject.FindObjectOfType<DataLogger>().LogSetMenuPin(pinned);
    }

    public void SetHologram()
    {
        Debug.Log("Setting hologram status to: " + hologramToggle.IsToggled);
        bimManager.SetVisibility(hologramToggle.IsToggled);
    }

    public void UpdateGUI(string taskNumber, string taskName, string instructions, Texture img)
    {
        // Set text values
        taskNumberMesh.text = taskNumber;
        taskNameMesh.text = taskName;
        instructionsMesh.text = instructions;
        // Load image and set the texture
        //Texture texture = Resources.Load<Texture>(imgName) as Texture;
        //imageQuadRenderer.material.mainTexture = texture;
        imageQuadRenderer.material.mainTexture = img;
}
}
