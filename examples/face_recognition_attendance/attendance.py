"""

 * Author:    Azmath Moosa
 * Created:   5th May 2018
 * Description: Performs face recognition and marks attendance
 * Dependencies: Deepsight Face, Python 3 packages:- requests, argparse, opencv-python, scipy
 
"""

import cv2
import requests
import numpy as np
import json
import argparse
import signal
import logging
import datetime, time
from scipy import spatial
import os

face_api = "http://127.0.0.1:5000/inferImage?returnFaceId=true&detector=yolo&returnFaceLandmarks=true"

# init logger
logger = logging.getLogger('Attendance')
logger.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(ch)

# attendance register
att_reg = []
try:
    att_reg = json.loads(open('att_log').read())
except:
    pass

# parse arguments
parser = argparse.ArgumentParser(description='Awesome Attendance System')
parser.add_argument('--enroll', action='store_true', help='Enable enrollment of unknown faces')
parser.add_argument('--src', action='store', default=0, nargs='?', help='Set video source; default is usb webcam')
parser.add_argument('--w', action='store', default=320, nargs='?', help='Set video width')
parser.add_argument('--h', action='store', default=240, nargs='?', help='Set video height')
args = parser.parse_args()

# initialize database
db = {"names":[],"embeddings":[]}
dbtree = ""
try:
    db = json.loads(open('att_db.txt').read())
    dbtree = spatial.KDTree(db["embeddings"])
except:
    pass

# start the camera
cap = cv2.VideoCapture(args.src)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, float(args.w))
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, float(args.h))
ret, frame = cap.read()

# catch exit signal
# in order to save attendance before exiting
def signal_handler(signal, frame):
    if args.enroll:
        logger.info("Saving Attendance DB")
        with open('att_db.txt','w') as att:
            att.write(json.dumps(db))
    
    logger.info("Saving attendance")
    with open('att_log','w') as att:
        att.write(json.dumps(att_reg, indent=4, sort_keys=True))

    exit(0)
signal.signal(signal.SIGINT, signal_handler)

    
# enroll a new face into db
def enroll(embedding, face):
    global dbtree
    cv2.imshow("New Face",face)
    cv2.waitKey(10)
    facename = input("New face detected, enter name:")    
    if facename != "":
        enroll.counter += 1
        if not os.path.exists("dbimg/%s"%(facename)):
            os.makedirs("dbimg/%s"%(facename))

        cv2.imwrite("dbimg/%s/%d.jpg"%(facename,enroll.counter), face)
        db["names"].append(facename)
        db["embeddings"].append(embedding)
        print("Enrolled %s into db!"%facename)

        dbtree = spatial.KDTree(db["embeddings"])

enroll.counter = 0

# search for a face in the db
def identify_face(embedding):
    if dbtree != "":
        dist, idx = dbtree.query(embedding)                               
        name = db["names"][idx]
        if dist > (0.4 if args.enroll else 0.5):
            name = "unknown"
    else:
        name = "unknown"
    
    return name


# returns minutes since
# last entry in attendance register
def mins_since_last_log():
    return ((datetime.datetime.now() - datetime.datetime.strptime(att_reg[-1]['time'], '%Y-%m-%d %H:%M:%S')).seconds/60)


# mark attendance
def mark_present(name):
    if len(att_reg) == 0: 
        logger.info("Detected %s"%name)
        stime = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        att = {'name':name,'time':stime}
        att_reg.append(att)
        return

    if att_reg[-1]['name'] != name or mins_since_last_log() > 1:
        logger.info("Detected %s"%name)
        stime = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        att = {'name':name,'time':stime}
        att_reg.append(att)        


# start processing
count = 0
while True:
    
    _, framex = cap.read()
    key = cv2.waitKey(1) & 0xFF

    count += 1
    if count % 2 != 0:
        continue

    frame = cv2.resize(framex, (int(args.w),int(args.h)))
    
    r, imgbuf = cv2.imencode(".bmp", frame)    
    image = {'pic':bytearray(imgbuf)}
    
    r = requests.post(face_api, files=image)
    result = r.json()

    if len(result) > 1:
        faces = result[:-1]
        diag = result[-1]['diagnostics']        
        #print(diag)

        for face in faces:
            rect, embedding = [face[i] for i in ['faceRectangle','faceEmbeddings']]
            x,y,w,h, confidence = [rect[i] for i in ['left', 'top', 'width', 'height', 'confidence']]

            if confidence < 0.8:
                continue

            name = identify_face(embedding)
            if args.enroll and name == "unknown":
                enroll(embedding, frame[y:y+h,x:x+w]) 
            else:
                if name != "unknown":
                    mark_present(name)

            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,255),5,8)        
            cv2.rectangle(frame, (x,y+h-20), (x+w,y+h), (255,0,255), -1, 8)
            cv2.putText(frame, "%s"%(name), (x,y+h), cv2.FONT_HERSHEY_DUPLEX, 1,  (255,255,255),2,8)
                        
        cv2.putText(frame, diag['elapsedTime'], (0,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255))                

    cv2.imshow("Attendance", frame)        
    if key == ord('q'):
        break

print("Exit")
