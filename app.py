from flask import Flask, render_template, make_response, request
from pymongo import MongoClient
import json
from flask_graphql import GraphQLView
from schema import schema
import datetime
from bson.objectid import ObjectId
from mongoengine import connect

app = Flask(__name__)
client: MongoClient = MongoClient(
    "localhost:27017")

db = client.user  # need for non graphql routes that access db

DEFAULT_CONNECTION_NAME = connect('user')  # need this for graphql

"""
initial endpoint for sample application 
all rendered templates need to be put in a templates folder 
"""


@app.route('/')
def index():
    return render_template("index.html")


"""
adds new user 
TODO: I don't like how this is done right now even though it works.
"""
@app.route('/user', methods=['POST'])
def add_users(*args):
    flag = False
    if args is not None:
        data = args[0]
        flag = True
    else:
        data = request.get_json("data")
    name = data["name"]
    image = request.files['img']
    user = {
        "name": name,
        "image": image,
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    result = db.user.insert_one(user)
    if flag:
        if result is not None:
            return "Success"
        raise RuntimeError(result)
    return make_response()


"""
removes new user 
"""
# @app.route('/user', methods=['DELETE'])
# def user():
#     # TODO :)

"""
returns all users 
"""
@app.route('/allUsers', methods=['GET'])
def get_all_users():
    entries = []
    cursor = db.user.find({})
    for document in cursor:
        document['_id'] = str(document['_id'])
        entries.append(document)

    return json.dumps(entries)


"""
given user_id, returns user 
"""
@app.route('/user/<user_id>', methods=['GET'])
def get_user_by_id(user_id: str):
    user = db.user.find_one({"_id": ObjectId(user_id)})
    user.pop('_id')
    return json.dumps(user)


"""
adds new known image
"""
@app.route('/known', methods=['POST'])
def add_known():
    data = request.get_json("data")
    img = data['img']
    name = data['name']
    known = {
        "name": name,
        "img": img
    }
    result = db.known.insert_one(known)
    return make_response()


"""
returns all known images
"""
@app.route('/known', methods=['GET'])
def get_all_known():
    entries = []
    cursor = db.known.find({})
    for document in cursor:
        document['_id'] = str(document['_id'])
        entries.append(document)

    return json.dumps(entries)


"""
adds new unknown image
"""
@app.route('/unknown', methods=['POST'])
def add_unknown():
    data = request.get_json("data")
    img = data['img']
    known = {
        "img": img
    }
    result = db.unknown.insert_one(known)
    return make_response()


"""
returns all unknown images
"""
@app.route('/unknown', methods=['GET'])
def get_all_unknown():
    entries = []
    cursor = db.unknown.find({})
    for document in cursor:
        document['_id'] = str(document['_id'])
        entries.append(document)

    return json.dumps(entries)


"""
graphql route
"""
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # for having the GraphiQL interface
    )
)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
