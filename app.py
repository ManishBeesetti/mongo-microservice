from random import seed
import pymongo
import traceback
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import json
import re
import hashlib
from datetime import datetime as dt
from flask_cors import CORS, cross_origin
import os


from flask import Flask, session
from flask import request
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['Secretkey'] = os.urandom(256)

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

@app.route('/signup',methods=["GET","POST"])
def signup():
    try:
        print("wassup")
        fname = request.args.get('fname')
        lname = request.args.get('lname')
        email = request.args.get('email')
        password = request.args.get('password')
        private_key = hashlib.sha256((email+str(dt.now())).encode('utf-8')).hexdigest()

        db = dbconnection('Agora_user_db')


        print(type(db))
        db.user.create_index([("email",pymongo.DESCENDING)],unique=True)
        print("here")
        collection = db.user
        print("here2")
        post = {
        'email' : email,
        'fname':fname,
        'lname':lname,
        'private_key' : private_key,
        'password': hashlib.sha256((password+private_key).encode('utf-8')).hexdigest()
        }
        print(post)
        print(collection)
        post_id = collection.insert_one(post).inserted_id
        # post_id = collection.insert_one(post)
        print("here3")
        return stat(0,'success') #signup successful
    except DuplicateKeyError:
        return stat(1,'exists') #user exists

    except:
        traceback.print_exc()
        return stat(-1,'failed') #db service issue

@app.route('/login',methods=["GET","POST"])
def login():

    try:
        email = request.args.get('email')
        password = request.args.get('password')
        db = dbconnection('Agora_user_db')
        collection = db.user
        doc = collection.find_one({"email":email})
        print("login" + str(doc))
        if (doc['password'] == hashlib.sha256((password+doc['private_key']).encode('utf-8')).hexdigest())  == 1 :
            return stat(0,os.urandom(256))
        else:
            return stat(2,'check password')


    except:
        traceback.print_exc()
        return stat(-1,"invalid username "+email)













if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
