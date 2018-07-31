"""

 * Author:    Azmath Moosa
 * Created:   31 July 2018
 * Description: Loads FIFA player embeddings and names from fifadb.json and loads them into faceDB.  It then 
                dumps database so that it can be used later.
 * Dependencies: Deepsight Face, FaceDB, python packages:- requests, argparse, opencv-python
 
"""

import json
import time
import requests

facedb_api = "http://localhost:5100/"
json_file = "fifadb.json"
facedb_dump_filename = "fifadb"

def load_db():
    data = json.loads(open(json_file).read())
    names = []
    embeddings = []
    for d in data:
        names.append(d['name'])
        embeddings.append(d['embedding'])
    
    return names, embeddings

def save_embeddings(names, embeddings):
    endpt = facedb_api + "save_embedding"
    t = time.time()
    count = 0    

    body = {"embeddings": embeddings, "metas": names}    
    res = requests.post(endpt,json=body)
    count = res.json()

    print(count, "items added in ", time.time() - t, "seconds")

def dump_database():
    endpt = facedb_api + "dump_database"
    t = time.time()
    res = requests.post(endpt, json={'filename':facedb_dump_filename})
    print("dump_database", res.json()," ", time.time() - t, "seconds")
    
if __name__ == "__main__":
    names, embeddings = load_db()
    print("items read " , len(names), len(embeddings))
    save_embeddings(names[:50], embeddings[:50])  #limited by 50 in free version of faceDB
    dump_database()    
    print("done")
