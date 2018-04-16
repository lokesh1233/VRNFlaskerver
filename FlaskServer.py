from flask import Flask
from Router.VRNRouter import VRNRouter 
from pymongo import MongoClient

client = MongoClient()
 
# Get the sampleDB database 
db = client.VRN

app = Flask(__name__)

VRNRouter(app, db)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=False)