This example demonstrates performing face recognition using deepsight SDK.

![face_detection](https://github.com/baseapp/DeepSight-Face-Recognition-SDK/blob/master/examples/face_recognition_attendance/usage.gif)


### Running

* To run this example, install the following dependencies

```sh
pip install requests 
pip install opencv-python
pip install scipy
```
* Next, start `Deepsight Face SDK` and let it run.
* First, perform face enrollment by running `python3 attendance.py --enroll`
* The application will prompt names for new faces.  Type a name and hit return.  If you don't want to enroll a face, hit return with empty name.
* Once you have enrolled enough faces, hit `Ctrl+C` to exit.
* Then run the application again as `python3 attendance.py` without `enroll` for marking attendance.
* The application will automatically log faces.  If the same face keeps appearing, it will wait a minute before marking it again.
* The application simply saves a time register in a json file called `att_log`

### Usage

* The application accepts arguments as follows

```sh
usage: attendance.py [-h] [--enroll] [--src [SRC]] [--w [W]] [--h [H]]

Awesome Attendance System

optional arguments:
  -h, --help   show this help message and exit
  --enroll     Enable enrollment of unknown faces
  --src [SRC]  Set video source; default is usb webcam
  --w [W]      Set video width
  --h [H]      Set video height
```

* `scale` arg tells how many times the image should be doubled in size.  This helps in detecting smaller faces.
* `det` arg tells which detector to use.  MMOD is more accurate but slow, YOLO is fast but has some false positives, HOG is fast for a CPU only system.  Default is MMOD.
* `src` arg points to the image.
