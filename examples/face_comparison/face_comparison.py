"""

 * Author:    Azmath Moosa
 * Created:   4th June 2018
 * Description: Performs face recognition and compares against a db
 * Dependencies: Deepsight Face, Python 3 packages:- requests, argparse, opencv-python, scipy, numpy
 
"""

import cv2
import requests
import numpy as np
import json
import argparse
import logging
import datetime, time
from scipy import spatial
import os
import glob
import utils

face_api = "http://127.0.0.1:5000/inferImage?returnFaceId=true&detector=mmod&returnFaceLandmarks=true"

# init logger
logger = logging.getLogger('FaceComparison')
logger.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(ch)


# parse arguments
parser = argparse.ArgumentParser(description='Face Comparison Application')
parser.add_argument('path', metavar='path', type=str, nargs='+',
                    help='path to image (or folder in scan mode)')
parser.add_argument('--scan', action='store_true', 
                    help='scan folder and create facedb')
args = parser.parse_args()

# initialize database
db = {"names":[],"embeddings":[]}
dbtree = ""
try:
    db = json.loads(open('facedb.json').read())
    # kdtree for similarity search
    dbtree = spatial.KDTree(db["embeddings"])
except:
    pass


def get_face_embedding_crop(imgpath):
    frame = cv2.imread(imgpath)

    # encode as bmp (optional)
    r, imgbuf = cv2.imencode(".bmp", frame)    
    image = {'pic':bytearray(imgbuf)}

    # post request
    r = requests.post(face_api, files=image)
    result = r.json()

    if len(result) == 2:
        faces = result[:-1]
        diag = result[-1]['diagnostics']
        #print(diag)

        for face in faces:
            rect, embedding = [face[i] for i in ['faceRectangle','faceEmbeddings']]
            x,y,w,h, confidence = [rect[i] for i in ['left', 'top', 'width', 'height', 'confidence']]

            if confidence < 0.8:
                continue

            crop = frame[y:y+h, x:x+w]

            return embedding, crop
    else:
        RuntimeError("no faces or more than 1 face in %s"%imgpath)

def save_db():
    with open("facedb.json","w") as f:
        f.write(json.dumps(db))

# search for a face in the db
def identify_face(embedding):
    if dbtree != "":
        dist, idx = dbtree.query(embedding)
        name = db["names"][idx]
        if dist > 0.6:
            name = "unknown"
    else:
        name = "unknown"
    
    return name

if __name__ == "__main__":

    if args.scan:
        db = {"names":[],"embeddings":[]}
        path = args.path[0]
        dirs = glob.glob(os.path.join(path, "*/"))
        for d in dirs:
            name = os.path.basename(os.path.dirname(d))
            imgs = glob.glob(os.path.join(d, "*.jpg"))
            imgs.extend(glob.glob(os.path.join(d,"*.png")))
            
            crops = []
            for img in imgs:
                try:
                    emb, crop = get_face_embedding_crop(img)
                    db["names"].append(name)
                    db["embeddings"].append(emb)
                    crops.append(crop)
                except Exception as e:
                    logger.error("ERROR:%s"%e)
            
            # convert image list into a montage of 256x256 images tiled in a 5x5 montage
            montages = utils.build_montages(crops, (150, 150), (2, 3))
            # iterate through montages and display
            for montage in montages:
                cv2.destroyAllWindows()
                cv2.imshow(name, montage)
                cv2.waitKey(1000)

        logger.info("Saved %d faces"%len(db["names"]))
        
        save_db()
        exit(0)
    else:

        for path in args.path:
            # start the camera
            emb, crop = get_face_embedding_crop(path)
            name = identify_face(emb)
            
            logger.info("Face in %s similar to %s"%(path, name))
            cv2.imshow("Input", crop)
            cv2.waitKey(4000)

print("Exiting")
