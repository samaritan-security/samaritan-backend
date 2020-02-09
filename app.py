from flask import Flask, render_template, make_response, request
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
"""
@app.route('/user', methods=['POST'])
def user():
    data = request.get_json("data")
    name = data["name"]
    image = data["image"]
    user = {
        "name": name,
        "image": image,
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    result = db.user.insert_one(user)
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
def get_users():
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
def get_user(user_id: str):
    user = db.user.find_one({"_id": ObjectId(user_id)})
    user.pop('_id')
    return json.dumps(user)


"""
graphql route
"""
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True   # for having the GraphiQL interface
    )
)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
