using System.Collections;
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

    void InitSocket()
    {
        lastSent = 0;
        //Listen to any IP, serve as a server
        ipEnd = new IPEndPoint(IPAddress.Any, 8001);
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
    string Vec2Str(Vector3 pos, Vector3 rot)
    {
        string output = pos.x.ToString("0.00") + ',';
        output += pos.z.ToString("0.00") + ',';
        output += pos.y.ToString("0.00") + ',';
        
        output += (-rot.z).ToString("0.00") + ',';
        output += (rot.x).ToString("0.00") + ',';
        output += (-rot.y + 90).ToString("0.00") + ',';
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

    // Update is called once per frame
    void Update()
    {
        //waiting for a client to connect
        if (!connected)
        {
            Thread.Sleep(500);
        }
        //after connected, send data till lost of connection
        else
        {
            //reduce data rate, only send at around 20Hz
            long currTicks = System.DateTime.Now.Ticks;

            if (currTicks - lastSent > 90 * 10000)
            {
                Vector3 camPos = targetCamera.position;
                Quaternion rotC = targetCamera.rotation;
                Vector3 camAngles = rotC.eulerAngles;

                Vector3 rightCtrlPos = rightController.position;
                Quaternion rotR = rightController.rotation;
                Vector3 rightAngles = rotR.eulerAngles;

                Vector3 leftCtrlPos = leftController.position;
                Quaternion rotL = leftController.rotation;
                Vector3 leftAngles = rotL.eulerAngles;

                long currMills = (currTicks - dtFrom.Ticks) / 10000;
                //  Data format: time stamp + 3 positions + 3 rotations

                sendStr = currMills.ToString() + "," + Vec2Str(camPos, camAngles);
                sendStr += "right, ";
                sendStr += Vec2Str(rightCtrlPos, rightAngles);
                sendStr += "left, ";
                sendStr += Vec2Str(leftCtrlPos, leftAngles);

                Debug.Log(rightAngles);
                Debug.Log(sendStr);
                //sendStr = "test";
                SocketSend(sendStr);
                lastSent = currTicks;
                Thread.Sleep(5);
            }
        }
    }

    void OnApplicationQuit()
    {
        SocketQuit();
    }
}