"""

 * Author:    Azmath Moosa
 * Created:   30th July 2018
 * Description: Python wrapper class for dsFace.  
                Please launch and run the dsFace separately
 * Dependencies: python requests, opencv-python, numpy
 
"""

import time
import json
import cv2
import requests
import numpy as np

face_api = "http://127.0.0.1:5000/inferImage?returnFaceId=true&detector=mmod&returnFaceLandmarks=true"



class DSFaceHandler():

    def __init__(self, api="http://127.0.0.1:5000/inferImage", face_rec=False, detector="mmod", face_lmk=False):
        print("Please make sure dsFace is running in the background (./dsFace )")
        self.face_api = api
        self.detector = detector
        self.faceRecognition = face_rec
        self.faceLmk = face_lmk
        

    def endpt(self):
        detector = "detector="+self.detector+"&"
        faceRecognition = "returnFaceId=true&" if self.faceRecognition else ""
        faceLmk = "returnFaceLandmarks=true" if self.faceLmk else ""
        
        return self.face_api + "?" + detector + faceRecognition + faceLmk

        
    def get_embedding(self, img):
        img = cv2.resize(img,(250,250))

        r, imgbuf = cv2.imencode(".bmp", img)    
        image = {'pic':bytearray(imgbuf)}
                    
        r = requests.post(self.endpt(), files=image)
        try:
            result = r.json()
        except Exception as e:
            print(e, r.text)

        if len(result) > 1:
            faces = result[:-1]
            diag = result[-1]['diagnostics']        

            for face in faces:
                rect, embedding = [face[i] for i in ['faceRectangle','faceEmbeddings']]
                x,y,w,h, confidence = [rect[i] for i in ['left', 'top', 'width', 'height', 'confidence']]

                if confidence < 0.5:
                    continue    

                crop = img[y:y+h, x:x+w]

                return np.asarray(embedding), crop
        else:
                return np.zeros([128]), img


