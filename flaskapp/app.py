from flask import Flask, render_template, make_response, request, jsonify
from pymongo import MongoClient
import json
from flask_graphql import GraphQLView

from Email import send_alert_email
from schema import schema
import datetime
from bson.objectid import ObjectId
from mongoengine import connect
import dateutil.parser
import traceback

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


"""returns all people"""


@app.route('/people', methods=['GET'])
def get_all_people(*args):
    entries = []
    cursor = db.people.find({})
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
gets all known people
"""


@app.route('/people/known', methods=['GET'])
def get_known_people(*args):
    entries = []
    cursor = db.people.find({"known": True})
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
gets all unknown people
"""


@app.route('/people/unknown', methods=['GET'])
def get_unknown_people(*args):
    entries = []
    cursor = db.people.find({"known": False})
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
adds new known person
"""


@app.route('/people/known', methods=['POST'])
def add_known_person(*args):
    flag = False
    if len(args) != 0:
        data = args[0]
        flag = True
    else:
        data = request.get_json("data")
    img = data["img"]
    npy = data["npy"]
    name = data["name"]
    known = True
    person = {
        "known": known,
        "name": name,
        "img": img,
        "npy": npy
    }
    result = db.people.insert_one(person)
    if flag:
        if result is not None:
            return "Success"
        raise RuntimeError(result)
    return make_response()


"""
adds new unknown person
"""


@app.route('/people/unknown', methods=['POST'])
def add_unknown_person(*args):
    flag = False
    if len(args) != 0:
        data = args[0]
        flag = True
    else:
        data = request.get_json("data")
    img = data['img']
    npy = data['npy']
    known = False
    person = {
        "known": known,
        "img": img,
        "npy": npy
    }
    result = db.people.insert_one(person)
    if flag:
        if result is not None:
            return "Success"
        raise RuntimeError(result)
    return make_response()


"""
given id, returns person
"""


@app.route('/people/<id>', methods=['GET'])
def get_person_by_id(id: str):
    entries = []
    cursor = db.people.find({"_id": ObjectId(id)})
    for document in cursor:
        document['_id'] = str(document['_id'])
        document['img'] = str(document['img'])
        document['npy'] = str(document['npy'])
        entries.append(document)

    response = jsonify(entries)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


"""
returns all instances of seen from s_time -> f_time
for a specific camera
"""


@app.route('/seen/<camera_id>/<s_time>/<f_time>', methods=['GET'])
def get_seen_time_interval(camera_id: str, s_time: str, f_time: str):
    s_time = s_time.replace("%", " ")
    f_time = f_time.replace("%", " ")

    start_time = dateutil.parser.parse(s_time)
    end_time = dateutil.parser.parse(f_time)

    entries = []
    cursor = db.seen.find({
        "camera_id": camera_id,
        "created_at": {
            "$gte": start_time,
            "$lte": end_time
        }})

    for document in cursor:
        document['_id'] = str(document['_id'])
        entries.append(document)

    response = jsonify(entries)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


"""
adds new seen
--internal use only--
"""


@app.route('/seen/<ref_id>', methods=['PUT'])
def add_new_seen(ref_id, camera_id):
    time = datetime.datetime.now()
    seen = {
        "ref_id": ref_id,
        "camera_id": camera_id,
        "created_at": time
    }
    result = db.seen.insert_one(seen)
    return result


"""
returns all in seen
"""


@app.route('/seen', methods=['GET'])
def get_all_seen():
    entries = []
    cursor = db.seen.find({})
    for document in cursor:
        document['_id'] = str(document['_id'])
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
removes given ref_id from authorized db
returns true if item deleted, false otherwise
"""


@app.route('/authorized/<ref_id>', methods=['DELETE'])
def remove_from_authorized(ref_id):
    result = db.authorized.delete_one({"_id": ref_id})
    response = jsonify(result.deleted_count == 1)
    response.headers.add('Acess-Control-Allow-Origin', '*')
    return response


"""
returns all authorized user ref_ids
(ref_id refers to the user's id in known or unknown)
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
removes given ref_id from unauthorized db
"""


@app.route('/unauthorized/<ref_id>', methods=['DELETE'])
def remove_from_unauthorized(ref_id):
    result = db.unauthorized.delete_one({"_id": ref_id})
    response = jsonify(result.deleted_count == 1)
    response.headers.add('Acess-Control-Allow-Origin', '*')
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
def check_for_unauthorized(ref_id: str):
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
returns all alerts instances from s_time => f_time
for a specific camera
"""


@app.route('/alerts/<camera_id>/<s_time>/<f_time>', methods=['GET'])
def get_alerts_time_interval(camera_id, s_time, f_time):
    s_time = s_time.replace("%", " ")
    f_time = f_time.replace("%", " ")

    start_time = dateutil.parser.parse(s_time)
    end_time = dateutil.parser.parse(f_time)

    entries = []
    cursor = db.alerts.find({
        "camera_id": camera_id,
        "created_at": {
            "$gte": start_time,
            "$lte": end_time
        }})

    for document in cursor:
        document['_id'] = str(document['_id'])
        entries.append(document)

    response = jsonify(entries)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


"""
adds new alert
--only accessed internally--
"""


@app.route('/alerts/<ref_id>/<email>', methods=['PUT'])
def add_new_alert(ref_id: str, camera_id: str, email: str):
    time = datetime.datetime.utcnow()
    alert = {
        "ref_id": ref_id,
        "camera_id": camera_id,
        "created_at": time
    }
    if len(email) > 0:
        image = get_person_by_id(alert.ref_id).image
        camera = get_camera_by_id(alert.camera_id)
        send_alert_email(alert, image, camera, email)
    result = db.alerts.insert_one(alert)
    return result


"""
returns all alerts
"""


@app.route('/alerts', methods=['GET'])
def get_all_alerts():
    entries = []
    cursor = db.alerts.find({})
    for document in cursor:
        document['_id'] = str(document['_id'])
        entries.append(document)

    response = jsonify(entries)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


"""
adds new camera to db
"""


@app.route('/camera', methods=['POST'])
def add_new_camera(*args):
    flag = False
    if len(args) != 0:
        data = args[0]
        flag = True
    else:
        data = request.get_json("data")
    ip = data['ip']
    nickname = data['nickname']
    camera = {
        "ip": ip,
        "nickname": nickname
    }
    result = db.cameras.insert_one(camera)
    if flag:
        if result is not None:
            return "Success"
        raise RuntimeError(result)
    return make_response()


"""
given camera_id, returns camera info
"""


@app.route('/camera/<camera_id>', methods=['GET'])
def get_camera_by_id(camera_id):
    entries = []
    cursor = db.cameras.find({"_id": ObjectId(camera_id)})
    for document in cursor:
        document['_id'] = str(document['_id'])
        entries.append(document)

    response = jsonify(entries)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


"""
returns all cameras
"""


@app.route('/camera', methods=['GET'])
def get_all_cameras(*args):
    flag = False
    if len(args) != 0:
        flag = True
    entries = []
    cursor = db.cameras.find({})
    for document in cursor:
        document["_id"] = str(document["_id"])
        entries.append(document)
    if flag:
        return entries
    response = jsonify(entries)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


"""
route to delete all known and unknown until we 
figure it out

TODO: remove this when stuff is good
"""


@app.route('/test', methods=['DELETE'])
def delete_all_known_unknown():
    db.authorized.remove({})
    db.unauthorized.remove({})
    db.seen.remove({})
    db.alerts.remove({})
    db.people.remove({})
    db.cameras.remove({})

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
