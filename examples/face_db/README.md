**Introducing FaceDB** - powered by Facebook Research's Search Similarity library, facedb is a binary that runs as a http service.  It stores embeddings in the millions and allows for searching the closest matching embedding within a second.

**What does it mean?**

It means that you can use FaceDB to query a face from a database of Million faces and expect results within a second.  This allows for highy scalable applications with an extremely easy to use API.

This example demonstrates usage of FaceDB to query an embedding from a DB of 50 faces of FIFA celebrities.  Please go through code to understand FaceDB usage.

> This example only works in Linux.  FaceDB is currently not available for Windows.  

> Free version of Face DB only supports 50 faces.

> Email us at contact@baseapp.com for further queries.

![face_db](https://github.com/baseapp/DeepSight-Face-Recognition-SDK/blob/master/examples/face_db/static/gen/2018-07-31_144814.jpg)


### Running

* To run this example, install the following dependencies

```sh
pip install requests 
pip install opencv-python
pip install scipy flask
```
* Next, start `Deepsight Face SDK` and let it run.
* Next, start `facedb --serve` and let it run
* Start the flask app using `python app.py`
* The application will say `fifa db initialized`
* Open a browser and point to `localhost:5101`
* Use the gui to upload a photo
* The application will return closest matching fifa celebrity

### Files

* `facedb` - This is the free version of faceDB binary.  It supports upto 50 faces.
* `app.py` - This is the flask app.
* `dsface.py` - A simple python wrapper to generate embeddings using Deepsight Face
* `facedb.py` - A simple python wrapper to `facedb` binary
*  `save_to_facedb.py` - This demonstrates how to save embeddings in `facedb`.  It reads values from `fifadb.json` and stores them in `facedb`.  It then dumps the database so that it can be loaded later.
