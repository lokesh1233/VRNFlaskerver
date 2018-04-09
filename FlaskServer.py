from flask import Flask
from Router.VRNRouter import VRNRouter 
from pymongo import MongoClient

client = MongoClient()
 
# Get the sampleDB database 
db = client.VRN

app = Flask(__name__)

VRNRouter(app, db)

if __name__ == "__main__":
    app.run('localhost',5000,True)