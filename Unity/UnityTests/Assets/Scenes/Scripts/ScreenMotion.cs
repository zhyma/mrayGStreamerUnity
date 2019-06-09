using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ScreenMotion : MonoBehaviour
{

    public Transform targetCamera;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        //transform.LookAt(targetCamera.position);
        transform.position = targetCamera.position + targetCamera.forward * 2;
        transform.rotation = Quaternion.LookRotation(targetCamera.position-transform.position)*Quaternion.Euler(0, 180, 0);
        //Debug.Log(targetCamera.forward);
        //Debug.Log(targetCamera.position);
    }
}
