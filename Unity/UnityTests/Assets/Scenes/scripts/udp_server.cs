using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

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
    Thread sendThread;

    //link to OVRCameraRig
    public Transform targetCamera;
    System.DateTime dtFrom = new System.DateTime(1970, 1, 1, 0, 0, 0, 0);


    void InitSocket()
    {
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
        sendThread = new Thread(new ThreadStart(DataSend));
        sendThread.Start();
    }

    string Vec2Str(Vector3 input)
    {
        string output = input.x.ToString() + ',';
        output += input.y.ToString() + ',';
        output += input.z.ToString() + ',';
        return output;
    }

    void DataSend()
    {
        Vector3 pos;
        Quaternion rotQ;
        Vector3 angles;

        while (true)
        {

        }
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
                recvLen = socket.ReceiveFrom(recvData, ref clientEnd);
            }
            catch
            {
                Debug.Log("remote closed");
                break;
            }
            Debug.Log("message from: " + clientEnd.ToString());
            recvStr = Encoding.ASCII.GetString(recvData, 0, recvLen);
            Debug.Log(recvStr);
        }
    }

    void SocketQuit()
    {
        if (receiveThread != null)
        {
            receiveThread.Interrupt();
            receiveThread.Abort();
        }
        if (sendThread != null)
        {
            sendThread.Interrupt();
            sendThread.Abort();
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
            lock (clientEnd)
            {
                string epString = clientEnd.ToString();
                string[] endPoint = epString.Split(':');
                IPAddress ip;
                IPAddress.TryParse(endPoint[0], out ip);
                int port;
                int.TryParse(endPoint[1], out port);
                if (port != 0)
                {
                    Debug.Log(endPoint[0]);
                    Debug.Log(endPoint[1]);
                    //copy client information
                    send2End = new IPEndPoint(ip, port);
                    connected = true;
                }
            }
        }
        //after connected, send data till lost of connection
        else
        {
            Vector3 pos = targetCamera.position;
            Quaternion rotQ = targetCamera.rotation;
            Vector3 angles = rotQ.eulerAngles;

            long currTicks = System.DateTime.Now.Ticks;
            long currMills = (currTicks - dtFrom.Ticks) / 10000;
            sendStr = currTicks.ToString() + "," + Vec2Str(pos) + Vec2Str(angles);
            Debug.Log(sendStr);
            //sendStr = "test";
            SocketSend(sendStr);
            //Thread.Sleep(10);
        }
    }

    void OnApplicationQuit()
    {
        SocketQuit();
    }
}