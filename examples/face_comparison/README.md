This example demonstrates performing face recognition using deepsight SDK.

![face_comparison](https://github.com/baseapp/DeepSight-Face-Recognition-SDK/blob/master/examples/face_comparison/usage.gif)


### Running

* To run this example, install the following dependencies

```sh
pip install requests 
pip install opencv-python
pip install scipy
```
* Next, start `Deepsight Face SDK` and let it run.
* In the folder `facedb/` add images of people you want to add to db
* Each person should have a separate folder
* Next, run the appliation with `python face_comparison.py --scan ./facedb/` to scan the folder and update the db
* Then, run the application with `python face_comparison.py <image_path>` to compare a new face with the db

### Usage

* The application accepts arguments as follows

```sh
usage: face_comparison.py [-h] [--scan] path [path ...]

Face Comparison Application

positional arguments:
  path        path to image (or folder in scan mode)

optional arguments:
  -h, --help  show this help message and exit
  --scan      scan folder and create facedb
```

* `scan` arg is used to scan a folder for new faces and save as a db.
* `path` arg points to the scanning folder path in scan mode or image path in comparison mode.
