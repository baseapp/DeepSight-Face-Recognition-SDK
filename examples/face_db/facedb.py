"""

 * Author:    Azmath Moosa
 * Created:   30th July 2018
 * Description: Python wrapper class for facedb.  
                Please launch and run the facedb app separately
 * Dependencies: python requests, json
 
"""
import json
import requests

class FaceDBHandler():

    def __init__(self, api="http://localhost:5100/", filename="facedb"):
        print("Please make sure facedb is running in the background( ./facedb --serve )")
        self.facedb_api = api
        self.db_path = filename

    def save_embedding(self, vec, meta):
        endpt = self.facedb_api + "save_embedding"
        body = {"embedding": vec, "meta":meta}    
        res = requests.post(endpt,json=body).json()
        return res

    def reindex(self):
        endpt = self.facedb_api + "reindex"
        res = requests.post(endpt, json={}).json()
        return res["message"] == "ok"
        
    def dump_database(self):
        endpt = self.facedb_api + "dump_database"        
        res = requests.post(endpt, json={"filename":self.db_path}).json()
        return res      

    def load_database(self):
        endpt = self.facedb_api + "load_database"
        res = requests.post(endpt, json={"filename":self.db_path}).json()
        return res["message"] == "ok"
                        
    def clear_database(self):
        endpt = self.facedb_api + "clear_database"
        res = requests.post(endpt, json={}).json()
        return res

    def print_database(self):
        endpt = self.facedb_api + "print_database"
        res = requests.post(endpt, json={}).json()
        return res

    def search_database(self, vec):
        endpt = self.facedb_api + "search_embedding"
        res = requests.post(endpt, json={"embedding": vec.tolist()})
        try:
            print(res.text)
            return res.json()
        except:
            return {"index":0, "distance":0.0}
        
            
