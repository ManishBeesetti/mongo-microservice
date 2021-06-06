import pymongo
import traceback
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask_cors import CORS, cross_origin
import json
import re

from flask import Flask
from flask import request
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def stat(code,description):
    return {
    'code' : code,
    'description' : description
    }

def dbconnection(database):
    try:
        url = "mongodb+srv://ruser:123@batserver.0hc30.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        client = MongoClient(url)
        print("connection successfull")
        return client.get_database(database)

    except:
        print("connection failed")

@cross_origin()
@app.route('/signup',methods=["GET","POST"])
def signup():
    try:
        print("wassup")
        username = request.args.get('user')
        password = request.args.get('pass')
        print(username)
        print(password)
        db = dbconnection('Agora_user_db')


        print(type(db))
        db.user.create_index([("uname",pymongo.DESCENDING)],unique=True)
        print("here")
        collection = db.user
        print("here2")
        post = {
        'uname' : username,
        'password': password
        }
        post_id = collection.insert_one(post).inserted_id
        print("here3")
        return stat(0,'success') #signup successful
    except DuplicateKeyError:
        return stat(1,'exists') #user exists

    except:
        traceback.print_exc()
        return stat(-1,'failed') #db service issue

@cross_origin()
@app.route('/login',methods=["GET","POST"])
def login():
    try:
        username = request.args.get('user')
        password = request.args.get('pass')
        db = dbconnection('Agora_user_db')
        collection = db.user
        doc = collection.find_one({"uname":username})
        print(doc)
        if doc['password'] == password:
            return stat(0,'success')
        else:
            return stat(1,'check password')


    except:
        traceback.print_exc()
        return stat(-1,"invalid username signup")

@cross_origin()
@app.route('/add',methods=["GET","POST"])
def add():
    try:
        username = request.args.get('user')
        link = request.args.get('link')
        db = dbconnection('Agora_user_db')
        collection = db.playlists
        db.playlists.create_index([("uname",pymongo.DESCENDING),("link",pymongo.ASCENDING)],unique=True)

        post = {
        "uname" : username,
        "link" : link
        }
        post_id = collection.insert_one(post).inserted_id
        return stat(0,'success') #insertion successful
    except DuplicateKeyError:
        return stat(1,'exists') #song exists
    except:
        traceback.print_exc()
        return stat(-1,'failed') #db service issue

@cross_origin()
@app.route('/play',methods=["GET","POST"])
def play():
    try:


        username = request.args.get('user')
        db = dbconnection('Agora_user_db')
        collection = db.playlists

        doc_li = [ str(doc).replace("\'", "\"") for doc in collection.find({"uname":username},{'_id':False})]

        dl2 = [json.loads(el)['link'] for el in doc_li]
        # for el in doc_li:
        #     dl2.append(json.loads(el)['link'])


        return stat(0,dl2)
    except:
        traceback.print_exc()
        return stat(-1,'failed to fetch')

















if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
