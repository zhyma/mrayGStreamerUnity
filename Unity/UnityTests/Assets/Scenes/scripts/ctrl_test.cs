using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Valve.VR;

public class ctrl_test : MonoBehaviour
{
    public SteamVR_Input_Sources LeftInputSource = SteamVR_Input_Sources.LeftHand;
    public SteamVR_Input_Sources RightInputSource = SteamVR_Input_Sources.RightHand;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        Debug.Log("Left Trigger value:" + SteamVR_Actions._default.Squeeze.GetAxis(LeftInputSource).ToString());
        Debug.Log("Right Trigger value:" + SteamVR_Actions._default.Squeeze.GetAxis(RightInputSource).ToString());
        Debug.Log("Left Trackpad value:" + SteamVR_Actions._default.Scroll.GetAxis(LeftInputSource).ToString());
        Debug.Log("Right Trackpad value:" + SteamVR_Actions._default.Scroll.GetAxis(RightInputSource).ToString());
    }
}


 
public class InputTester : MonoBehaviour
{




}