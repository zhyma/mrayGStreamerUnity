﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

using Valve.VR;

public class udp_server : MonoBehaviour
{
    Socket socket;
    EndPoint clientEnd;//obtain client information
    EndPoint send2End;//used for sending data to the client
    IPEndPoint ipEnd;
    bool connected = false;
    string recvStr;
    string sendStr;
    byte[] recvData = new byte[1024];
    byte[] sendData = new byte[1024];
    int recvLen;
    Thread receiveThread;

    //link to OVRCameraRig
    public Transform targetCamera;
    public Transform leftController;
    public Transform rightController;
    System.DateTime dtFrom = System.DateTime.Now;
    //System.DateTime dtFrom = System.DateTime.Now.Ticks;
    long lastSent;

    public SteamVR_Input_Sources LeftInputSource = SteamVR_Input_Sources.LeftHand;
    public SteamVR_Input_Sources RightInputSource = SteamVR_Input_Sources.RightHand;

    void InitSocket()
    {
        lastSent = 0;
        //Listen to any IP, serve as a server
        ipEnd = new IPEndPoint(IPAddress.Any, 23023);
        socket = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
        socket.Bind(ipEnd);

        //define a connection after hearing from a client and send message to that client 
        IPEndPoint sender = new IPEndPoint(IPAddress.Any, 0);
        clientEnd = (EndPoint)sender;
        print("waiting for UDP dgram");

        //thread for hearing from client
        receiveThread = new Thread(new ThreadStart(SocketReceive));
        receiveThread.Start();

        //send 6DOFs head information to the client
        //sendThread = new Thread(new ThreadStart(DataSend));
        //sendThread.Start();
    }

    //1. Convert the vectors from the Unity coordinate to the ROS coordinate
    //2. convert the "corrected vectors" to string, prepare for the UDP package.
    //giving x, y, z, roll, pitch, yaw
    string Vec2Str(Vector3 pos, Quaternion rot)
    {
        string output = (-pos.z).ToString("0.00") + ',';
        output += pos.x.ToString("0.00") + ',';
        output += pos.y.ToString("0.00") + ',';
        
        output += (-rot.z).ToString("0.0000") + ','; 
        output += (rot.x).ToString("0.0000") + ',';
        output += (-rot.y).ToString("0.0000") + ',';
        output += (rot.w).ToString("0.0000") + ',';
        return output;
    }

    void SocketSend(string sendStr)
    {
        //clean up send buffer
        sendData = new byte[1024];
        //data conversion
        sendData = Encoding.ASCII.GetBytes(sendStr);
        //send data
        try
        {
            socket.SendTo(sendData, sendData.Length, SocketFlags.None, clientEnd);
        }
        catch
        {
            Debug.Log("remote closed.");
            connected = false;
        }
    }

    //receive from a client
    void SocketReceive()
    {
        while (true)
        {
            //clean up buffer
            recvData = new byte[1024];
            //receive data and get client information
            try
            {
                Debug.Log("Try to receive");
                recvLen = socket.ReceiveFrom(recvData, ref clientEnd);
                Debug.Log("Message from: " + clientEnd.ToString());
                recvStr = Encoding.ASCII.GetString(recvData, 0, recvLen);
                Debug.Log(recvStr);
                connected = true;
            }
            catch
            {
                Debug.Log("Remote closed. Receive failed");
                connected = false;
            }
        }
    }

    void SocketQuit()
    {
        if (receiveThread != null)
        {
            receiveThread.Interrupt();
            receiveThread.Abort();
        }
        if (socket != null)
            socket.Close();
        Debug.Log("disconnect");
    }

    // Start is called before the first frame update
    void Start()
    {
        InitSocket();
    }

    void BtnState(bool state)
    {
        if (state)
            sendStr += "1, ";
        else
            sendStr += "0, ";
    }

    // Update is called once per frame
    void Update()
    {
        //waiting for a client to connect
        if (!connected)
        {
            Thread.Sleep(20);
        }
        //after connected, send data till lost of connection
        else
        {
            //reduce data rate, only send at around 10Hz
            long currTicks = System.DateTime.Now.Ticks;

            if (currTicks - lastSent > 180 * 10000)
            {
                Vector3 camPos = targetCamera.position;
                Quaternion rotH = targetCamera.rotation;

                Vector3 rightCtrlPos = rightController.position;
                Quaternion rotR = rightController.rotation;

                Vector3 leftCtrlPos = leftController.position;
                Quaternion rotL = leftController.rotation;

                long currMills = (currTicks - dtFrom.Ticks) / 10000;
                //  Data format: time stamp + 3 positions + 4 quaternion rotations

                sendStr = currMills.ToString() + "," + Vec2Str(camPos, rotH);
                sendStr += "right, ";
                sendStr += Vec2Str(rightCtrlPos, rotR);
                sendStr += "left, ";
                sendStr += Vec2Str(leftCtrlPos, rotL);
                sendStr += "r_ctrl, ";
                sendStr += SteamVR_Actions._default.TrackpadAxis.GetAxis(RightInputSource)[0].ToString("0.00") + ", ";
                sendStr += SteamVR_Actions._default.TrackpadAxis.GetAxis(RightInputSource)[1].ToString("0.00") + ", ";
                sendStr += SteamVR_Actions._default.TriggerAxis.GetAxis(RightInputSource).ToString("0.00") + ", ";
                BtnState(SteamVR_Actions._default.Menu.GetState(RightInputSource));
                BtnState(SteamVR_Actions._default.TriggerBtn.GetState(RightInputSource));
                BtnState(SteamVR_Actions._default.TrackpadBtn.GetState(RightInputSource));
                BtnState(SteamVR_Actions._default.Grip.GetState(RightInputSource));
                //BtnState(SteamVR_Actions._default.System.GetState(RightInputSource));

                sendStr += "l_ctrl, ";
                sendStr += SteamVR_Actions._default.TrackpadAxis.GetAxis(LeftInputSource)[0].ToString("0.00") + ", ";
                sendStr += SteamVR_Actions._default.TrackpadAxis.GetAxis(LeftInputSource)[1].ToString("0.00") + ", ";
                sendStr += SteamVR_Actions._default.TriggerAxis.GetAxis(LeftInputSource).ToString("0.00") + ", ";
                BtnState(SteamVR_Actions._default.Menu.GetState(LeftInputSource));
                BtnState(SteamVR_Actions._default.TriggerBtn.GetState(LeftInputSource));
                BtnState(SteamVR_Actions._default.TrackpadBtn.GetState(LeftInputSource));
                BtnState(SteamVR_Actions._default.Grip.GetState(LeftInputSource));

                Debug.Log(sendStr);
                SocketSend(sendStr);
                lastSent = currTicks;
                Thread.Sleep(50);
            }
        }
    }

    void OnApplicationQuit()
    {
        SocketQuit();
    }
}