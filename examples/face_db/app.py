"""

 * Author:    Azmath Moosa
 * Created:   31st July 2018
 * Description: Flask app to demonstrate use of FaceDB.  
                This app can be accessed at localhost:5101
                It takes an image and finds the closest matching
                FIFA celebrity.
                It uses Deepsight SDK for face detection and retrieves embeddings.
                It then uses FaceDB to query the closest embeddings and retrieves celeb name.
                It then shows the celeb's photo next to the input photo.
                Please launch and run facedb and dsFace manually
 * Dependencies: python requests, json, flask, opencv-python, numpy
 
"""

from flask import Flask, render_template, request, make_response, Markup, send_from_directory
import io
import numpy as np
import cv2
import utils
import base64
import datetime
from facedb import FaceDBHandler
from dsface import DSFaceHandler

app = Flask(__name__)

faceDB = FaceDBHandler(filename="fifadb")
dsFace = DSFaceHandler(face_rec=True,face_lmk=True)


@app.route("/")
def index():
   return render_template("input.html")

@app.route("/result", methods=['POST'])
def result():
    photo = request.files['face']
    in_memory_file = io.BytesIO()
    photo.save(in_memory_file)
    data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
    color_image_flag = 1
    img = cv2.imdecode(data, color_image_flag)    

    vec, crop = dsFace.get_embedding(img)

    search = faceDB.search_database(vec)

    print(search)

    celebname = search["meta"]

    output_img = utils.read_transparent_png("static/pics/%s.png"%celebname)
    outimg = utils.build_montages([crop, output_img], (180,180),(2,1))    
    fname = "static/gen/"+datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S') + ".jpg"
    cv2.imwrite(fname, outimg[0])

    return render_template("result.html", name=celebname, imgpath = fname)

@app.route('/<path:path>')
def send_file(path):
    return send_from_directory('.', path)


if __name__ == "__main__":
    if faceDB.load_database():
        faceDB.reindex()
        print("fifa db initialized")
        app.run(host= '0.0.0.0', port=5101)
    else:
        print("Failed to load and init fifa database; is fifadb.db and fifadb.index files present?\
        Use save_to_facedb.py to generate them")
