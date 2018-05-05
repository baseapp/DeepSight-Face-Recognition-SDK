"""

 * Author:    Azmath Moosa
 * Created:   5th May 2018
 * Description: Performs face detection using Deepsight Face SDK and draws boxes around them
 * Dependencies: Deepsight Face, python packages:- requests, argparse, opencv-python
 
"""

import requests # for making http requests
import argparse # for making argument parsers
import cv2      # for image manipulation

parser = argparse.ArgumentParser(description='face_detection')
parser.add_argument('--det', action='store', default="mmod", nargs='?', help='Detector `mmod` or `yolo` or `hog` ')
parser.add_argument('--scale', action='store', default=0, nargs='?', help='Double the image size N times to detect smaller faces, 0=1xSize, 1=2xSize, 2=4xSize')
parser.add_argument('--src', action='store', default=0, nargs='?', help='Set source image')
args = parser.parse_args()

face_api="http://localhost:5000/inferImage?detector=%s&dblScale=%d"%(args.det,args.scale)

try:
    img = cv2.imread(args.src)
except:
    print("Critical: failed to read image")
    exit(1)
    
frame = cv2.imread(args.src)    
r, imgbuf = cv2.imencode(".bmp", frame)    
image = {'pic':bytearray(imgbuf)}
r = requests.post(face_api,files=image)
result = r.json()

# The result is a list as follows 
# [{face1},
#  ...
# {faceN},
# {diagnostics}]
if len(result) < 2:
    print("No detections! Try image with larger face! or try next tutorial with advanced request params") 
else:    
    faces = result[:-1]
    diag = result[-1]['diagnostics']        
    #print(diag)

    for face in faces:
        rect = [face[i] for i in ['faceRectangle']][0]
        x,y,w,h, confidence = [rect[i] for i in ['left', 'top', 'width', 'height', 'confidence']]

        if confidence < 0.8:
            continue

        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,255),5,8)        
               
    cv2.putText(frame, diag['elapsedTime'], (0,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255))
       

for i,face in enumerate(result[:-1]):
    print("Face %d  "%i, face)
    

cv2.imshow("face_detection", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
