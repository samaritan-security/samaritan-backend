import pickle

import pymongo
from flask import Flask, render_template, make_response, request, jsonify
from pymongo import MongoClient
import json
from flask_graphql import GraphQLView
from schema import schema
import datetime
from bson.objectid import ObjectId
from mongoengine import connect

app = Flask(__name__)
client: MongoClient = MongoClient("localhost:27017")

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
DEPRECATED ATM
"""
# @app.route('/user', methods=['POST'])
# def add_users(*args):
#     flag = False
#     if args is not None:
#         data = args[0]
#         flag = True
#     else:
#         data = request.get_json("data")
#     name = data["name"]
#     image = data["image"]
#     user = {
#         "name": name,
#         "image": image,
#         "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     }
#     result = db.user.insert_one(user)
#     if flag:
#         if result is not None:
#             return "Success"
#         raise RuntimeError(result)
#     return make_response()


"""
returns all users
DEPRECATED
"""
# @app.route('/allUsers', methods=['GET'])
# def get_all_users():
#     entries = []
#     cursor = db.user.find({})
#     for document in cursor:
#         document['_id'] = str(document['_id'])
#         entries.append(document)
#     return json.dumps(entries)


"""
given user_id, returns user
deprecated
"""
# @app.route('/user/<user_id>', methods=['GET'])
# def get_user_by_id(user_id: str):
#     user = db.user.find_one({"_id": ObjectId(user_id)})
#     user.pop('_id')
#     return json.dumps(user)


"""
adds new known name and image to stream.
the stream represents the current
known people in the camera feed.
"""
@app.route('/known', methods=['POST'])
def add_known_to_stream(*args):
    flag = False
    if len(args) != 0:
        data = args[0]
        flag = True
    else:
        data = request.get_json("data")
    img = data['img']
    name = data['name']
    npy = data['npy']
    known = {
        "name": name,
        "img": img,
        "npy": npy
    }
    # result = db.known.insert_one(known)
    result = db.known.update_one({
        'name': known['name']
    }, {
        '$set': {
            'name': known['name'],
            'img': known['img'],
            'npy': known['npy']
        }
    }, upsert=True)
    if flag:
        if result is not None:
            return "Success"
        raise RuntimeError(result)
    return make_response()


"""
returns all known images
"""
@app.route('/known', methods=['GET'])
def get_all_known(*args):

    entries = []
    cursor = db.known.find({})
    for document in cursor:
        document['_id'] = str(document['_id'])
        document['img'] = str(document['img'])
        document['npy'] = str(document['npy'])
        entries.append(document)

    if len(args) == 0:
        response = jsonify(entries)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    return entries


"""
adds new unknown image to stream.
the stream represents the current
unknown people in the camera feed.
"""
@app.route('/unknown', methods=['POST'])
def add_unknown_to_stream(*args):
    flag = False
    if len(args) != 0:
        data = args[0]
        flag = True
    else:
        data = request.get_json("data")
    img = data['img']
    npy = data['npy']
    known = {
        "img": img,
        "npy": npy
    }
    # result = db.unknown.insert_one(known)
    result = db.unknown.update_one({
        'img': known['img'],
        'npy': known['npy']
    }, {
        '$set': {
            'img': known['img'],
            'npy': known['npy']
        }
    }, upsert=True)
    if flag:
        if result is not None:
            return "Success"
        raise RuntimeError(result)
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
        document['img'] = str(document['img'])
        document['npy'] = str(document['npy'])
        entries.append(document)

    response = jsonify(entries)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


"""
adds to authorized
returns 200 if added, 500 if duplicate id
"""
@app.route('/authorized', methods=['POST'])
def add_authorized():
    data = request.get_json("data")
    ref_id = data["ref_id"]
    authorized = {
        "_id": ref_id
    }
    try:
        result = db.authorized.insert_one(authorized)
    except:
        return app.response_class(
            status=500,
            mimetype='application/json'
        )
    return app.response_class(
        status=200,
        mimetype='application/json'
    )


"""
adds to unauthorized
returns 200 if added, 500 if duplicate id
"""
@app.route('/unauthorized', methods=['POST'])
def add_unauthorized():
    data = request.get_json("data")
    ref_id = data["ref_id"]
    unauthorized = {
        "_id": ref_id
    }
    try:
        result = db.unauthorized.insert_one(unauthorized)
    except:
        return app.response_class(
            status=500,
            mimetype='application/json'
        )
    return app.response_class(
        status=200,
        mimetype='application/json'
    )


"""
returns all authorized user ref_ids
(reF_id referes to the user's id in known or unknown)
"""
@app.route('/authorized', methods=['GET'])
def get_all_authorized():
    entries = []
    cursor = db.authorized.find({})
    for document in cursor:
        document["_id"] = str(document["_id"])
        entries.append(document)
    response = jsonify(entries)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


"""
returns all unauthorized user ref-ids
(ref_id refers to the user's id in known or unknown)
"""
@app.route('/unauthorized', methods=['GET'])
def get_all_unauthorized():
    entries = []
    cursor = db.unauthorized.find({})
    for document in cursor:
        document["_id"] = str(document["_id"])
        entries.append(document)
    response = jsonify(entries)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


"""
checks if a ref_id exists in the unauthorized db.
returns True if exists, False otherwise
"""
@app.route('/unauthorized/<ref_id>', methods=['GET'])
def check_for_unauthorized(ref_id : str):
    result = db.unauthorized.find({"_id": ref_id})
    result_count = result.count()
    if result_count < 1:
        response = False
    else:
        response = True
    return app.response_class(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )


"""
removes ref_id from authorized db
"""
@app.route('/authorized/<ref_id>', methods=['DELETE'])
def remove_from_authorized(ref_id : str):
    result = db.authorized.remove({"ref_id" : ref_id})
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


"""
removed given ref_id from unauthorized db
"""
@app.route('/unauthorized/<ref_id>', methods=['DELETE'])
def remove_from_unauthorized(ref_id : str):
    result = db.unauthorized.remove({"ref_id" : ref_id})
    response = jsonify(result)
    response.headers.add('Acess-Control-Allow-Origin', '*')
    return response


"""
route to delete all known and unknown until we 
figure it out

TODO: remove this when stuff is good
"""
@app.route('/test', methods=['DELETE'])
def delete_all_known_unknown():
    db.unknown.remove({})
    db.known.remove({})
    db.authorized.remove({})
    db.unauthorized.remove({})

    return make_response()


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
