# mrayGStreamerUnity
GStreamer Integration with Unity using a Native plugin 

Updated 11/April/2017:

Currently designed to run under Unity 64bit version - Windows
The current integration implements a GStreamer H264 UDP receiver texture inside Unity. 

To compile the plugin:

1- Download and install (Complete, preferebly to C:\) gstreamer 1.0 runtimes 64bit (tested on 1.11.x - x86_64)

http://gstreamer.freedesktop.org/data/pkg/windows/

2- Install Visual studio runtimes x64 version:
> VS 2010:
https://www.microsoft.com/en-US/Download/confirmation.aspx?id=14632
> VS 2013:
https://www.microsoft.com/en-us/download/details.aspx?id=40784


3- [Important] Add gstreamer binary folder path to System Environment Variables:

Computer -> System properties -> Advanced System Settings -> Advanced Tab -> Environment Variables... -> System Variables -> Variable: Path -> Edit -> New -> C:\gstreamer\1.0\x86_64\bin


GStreamer path should be similar to this (depending on installation directory):
C:\gstreamer\1.0\x86_64\bin

4- [Optional] Compile using Visual studio 2013 and put the result dll into Plugins/x86_64 Unity folder (or use the already compiled dll in the Plugins/x86_64 folder)

5- Open test scenes and check the info text 

----
## Modification

Add asset "Oculus Integration" to the given example (mrayGStreamerUnity/UnityTests). Modify scenes to stream video through the network and transport Oculus' HMD.

Run batch file "mjpeg_test.bat" for test the function of video streaming. Or modify the command line for other video sources/OS.

The Unity project runs as a server. The "py3dplot/realtime_udp.py" (under the root folder) is an example of visualizing the x, y, z and roll, pitch, yaw of the HMD. The connection is established through port 8001, UDP. The data is a string, contains timestamp, x, y, z, rotation alone x, rotation alone y, rotation alone z directly pull from Unity, OVRCameraRig, CenterEyeAnchor. Each value is seperated by comma. Note that the coordinate in left-handed, and the unit of angles is in degree.
