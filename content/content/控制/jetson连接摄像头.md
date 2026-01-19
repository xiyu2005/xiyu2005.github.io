---
draft: false
---

sudo /opt/nvidia/jetson-io/jetson-io.py
![[Pasted image 20250921154853.png]]
选24pin csi connector设置
![[Pasted image 20250921154921.png]]
选第一个，然后回车回车，确认重启
即可
测试命令与日志
```
xiyu@ubuntu:~/Desktop$ gst-launch-1.0 nvarguscamerasrc num-buffers=1 ! 'video/x-raw(memory:NVMM),width=1280, height=720' ! nvjpegenc ! filesink location=final_test.jpg
Setting pipeline to PAUSED ...
Pipeline is live and does not need PREROLL ...
Pipeline is PREROLLED ...
Setting pipeline to PLAYING ...
New clock: GstSystemClock
GST_ARGUS: Creating output stream
CONSUMER: Waiting until producer is connected...
GST_ARGUS: Available Sensor modes :
GST_ARGUS: 3280 x 2464 FR = 21.000000 fps Duration = 47619048 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;

GST_ARGUS: 3280 x 1848 FR = 28.000001 fps Duration = 35714284 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;

GST_ARGUS: 1920 x 1080 FR = 29.999999 fps Duration = 33333334 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;

GST_ARGUS: 1640 x 1232 FR = 29.999999 fps Duration = 33333334 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;

GST_ARGUS: 1280 x 720 FR = 59.999999 fps Duration = 16666667 ; Analog Gain range min 1.000000, max 10.625000; Exposure Range min 13000, max 683709000;

GST_ARGUS: Running with following settings:
   Camera index = 0 
   Camera mode  = 4 
   Output Stream W = 1280 H = 720 
   seconds to Run    = 0 
   Frame Rate = 59.999999 
GST_ARGUS: Setup Complete, Starting captures for 0 seconds
GST_ARGUS: Starting repeat capture requests.
CONSUMER: Producer has connected; continuing.
NvMMLiteBlockCreate : Block : BlockType = 1 
Redistribute latency...
Got EOS from element "pipeline0".
Execution ended after 0:00:00.368850284
Setting pipeline to NULL ...
GST_ARGUS: Cleaning up
CONSUMER: Done Success
GST_ARGUS: Done Success
Freeing pipeline ...
```
![[Pasted image 20250921155200.png]]
拍摄成功～