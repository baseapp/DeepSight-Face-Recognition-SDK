This simple example demonstrates performing face detection using deepsight SDK.

![face_detection](https://github.com/baseapp/DeepSight-Face-Recognition-SDK/blob/master/examples/face_detection/usage.gif)


### Running

* To run this example, install the following dependencies

```sh
pip install requests 
pip install opencv-python
```

* Next, start `Deepsight Face SDK` and let it run.
* Then run this application `python face_detection.py --src C:\\path\\to\\image.jpg`

### Usage

* The application accepts arguments as follows

```sh
usage: face_detection.py [-h] [--det [DET]] [--scale [SCALE]] [--src [SRC]]

face_detection

optional arguments:
  -h, --help       show this help message and exit
  --det [DET]      Detector `mmod` or `yolo` or `hog`
  --scale [SCALE]  Double the image size N times to detect smaller faces,
                   0=1xSize, 1=2xSize, 2=4xSize
  --src [SRC]      Set source image

```

* `scale` arg tells how many times the image should be doubled in size.  This helps in detecting smaller faces.
* `det` arg tells which detector to use.  MMOD is more accurate but slow, YOLO is fast but has some false positives, HOG is fast for a CPU only system.  Default is MMOD.
* `src` arg points to the image
