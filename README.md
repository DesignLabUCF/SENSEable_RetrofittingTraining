# BIM-enabled AR Retrofitting Training

Augmented Reality (AR) tools have shown significant potential in providing on-site visualization of Building Information Modeling (BIM) data and models for supporting construction evaluation, inspection, and guidance. Retrofitting existing buildings, however, remains a challenging task requiring more innovative solutions to successfully integrate AR and BIM.  This project is focused on integrating AR+BIM for the retrofitting training process and assess the potential for future on-site usage.

[Video Demonstration](https://youtu.be/2iTBAz5ummA)

For our full paper, see **TODO**.

| [SENSEable Design Lab](https://sdl.eecs.ucf.edu/) | [UCF Modeling & Simulation](https://www.ist.ucf.edu/)  |
|--------|--------|
|    ![SENSEableDesign Lab](GitHubGraphics/SENSEable.png)    |    ![UCF](GitHubGraphics/UCF.png)    |
|   |   |


## Toolset

This project was designed in **Unity** for the **Microsoft HoloLens 2** and currently is only compatible with it.

To run, first install all necessary pre-requisite [**Visual Studio 2022 workloads**](https://learn.microsoft.com/en-us/windows/mixed-reality/develop/install-the-tools) and [**Unity 2020.3.34f1 ** with essential engine components](https://learn.microsoft.com/en-us/windows/mixed-reality/develop/unity/choosing-unity-version). More recently updated versions of the Unity 2020.3 LTS should be supported as well, however this has not been tested. Interface systems and interactions were created using [**MRTK version 2.82**](https://learn.microsoft.com/en-us/windows/mixed-reality/develop/unity/new-openxr-project-with-mrtk), which comes bundled in these project files.

The process to build and deploy the application to a HoloLens 2 is best explained in [Microsoft's Documentation](https://learn.microsoft.com/en-us/windows/mixed-reality/develop/advanced-concepts/using-visual-studio?tabs=hl2).

This project can be adapted to other environments by altering Unity scripts and objects. The main scene in the current build is *WorldLocked*. 3D models which will be aligned to a QR code should be added as a child object to the *AlignmentManager* gameobject. The the top-left corner of the front surface of the objects should align with *AlignmentManager*'s position (which by default is at [0,0,0]). Next, set the *Root Object* variable on the *BIMManager* script to be the new model's base object. Tasks are added new *Task* prefabs to the *TaskList* objects. After setting the task name, number, instructions, and image, you can add new task visuals as child objects to its *Holograms* child object. These visuals will only be visible when that task is currently active.

## Current Application Workflow

The study administrator menu is accessible by facing the right palm up towards the camera while flat.

1. Launch application.
2. Scan any QR code 100 times.
3. Perform manual adjustments by grabbing and rotating the axis arrows at the QR's location (optional).
4. On the administrator menu, and select the *Lock Wall* button to remove adjustment axis.
5. Do tasks.
6. Save data. This will be done automatically when a task name "End" is reached, but it is recommended to save using the *Write Data* button on the administrator menu. You can tell saving is happening by the progress number above the button incrementing.
7. Data is saved to the [applications persistent data path](https://docs.unity3d.com/ScriptReference/Application-persistentDataPath.html) in the *OutputData* folder.

## Data Processing

Data processing is primarly done using **Python 3.8.10**. A description of the directory's workflow and organization is found in [*Data*](Data) folder.

## Pre/Post-Questionnaire Surveys

Screen captures from the Qualtrics pre and post questionnaires that participants completed are found in *[StudyMaterials/QuestionnaireCaptures](StudyMaterials/QuestionnaireCaptures)*. Not included are the post-questionnaire *SUS*, *NASA TLX*, *VVIQ*, *VVSQ*, *OSVIQ*, and *Spatial Ability Test*.
