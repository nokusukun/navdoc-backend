import json
import secrets
import arrow
from pprint import pprint
from flask import Blueprint, render_template, abort, jsonify
from flask import Flask, send_from_directory, request, session, redirect, send_file, url_for
from flask_cors import CORS

from models import clinic
from models import errors
from base import utils
from base import QueryOp as query
from functools import wraps


prefix = "/clinic"
db = None
com = Blueprint("clinic", __name__)
CORS(com)
masterdb = None

sess = None
s_data = lambda : sess[request.headers["Session-Token"]]

def Load(_app, _db, session_data):
    global db, sess, masterdb
    db      = _db.clinic
    app     = _app
    masterdb= _db
    sess = session_data
    _app.register_blueprint(com, url_prefix=prefix)


def require_login(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        print(f"[{f.__name__}] This endpoint requires to be logged in.")
        token = request.headers.get("Session-Token")
        if not token or token not in sess:
            abort(400, errors.account.e08)
        print(token)
        #pprint(session.__dict__)
        if sess[token].get("uid") is None:
            print("Endpoint access failed.")
            abort(400, errors.account.e00)
        else:
            print("Endpoint access success.")
            return f(*args, **kwargs)
    return wrap


# Delete on production
@com.route("/delete_all")
def account_delete():
    db.collection.drop()
    return jsonify({"Success": "RIP Clinic Database"})


@com.route("/create", methods=["GET", "POST"])
@require_login
def clinic_add():
    required = ["city", "address", "hours", "contact_number", "coordinates"]
    data = request.get_json(force=True)

    new_clinic = clinic.Clinic(data)
    val = new_clinic.validate(required)
    if val:
        abort(400, errors.account.e02 + [val])

    new_clinic.uid = secrets.token_hex(8)
    new_clinic.author = s_data()["uid"]
    new_clinic.active = True
    result = db.add(new_clinic)

    if errors.db.iserror(result):
        abort(400, result)

    new_clinic.__dict__["success"] = True
    return jsonify(new_clinic.to_dict())


@com.route("/get/<clinic_id>", methods=["GET", "POST"])
@require_login
def clinic_get(clinic_id):

    result = db.get_one(uid=clinic_id)
    if result.uid == None:
        abort(400, errors.clinic.e00)
    result.__dict__["doctors"] = [x.to_dict() for x in masterdb.account.get_many(account_type="doctor", clinic=result.uid)]


    return jsonify(result.to_dict())


@com.route("/update/<clinic_id>", methods=["POST"])
@require_login
def clinic_update(clinic_id):

    data = request.get_json(force=True)
    restricted_types = ["city", "address", "hours", "contact_number", "coordinates"]
    for r_type in restricted_types: 
        if r_type in data: 
            data.pop(r_type)

    clinic_data = db.get_one(uid=clinic_id)
    if clinic_data.author != s_data()["uid"]:
        abort(400, errors.clinic.e01)
    pprint(clinic_data.to_dict())
    result = db.update(clinic_data, data)
    if result is None:
        abort(400, errors.account.e07)


@com.route("/search", methods=["POST"])
@require_login
def clinic_get_province():
    data = request.get_json(force=True)
    #list(x.collection.find({"username": query.Regex(".*Michael.*")}))
    #for key in data:
    #    data[key] = query.Regex(f".*{data[key]}.*")
    #    data[key]["$options"] = '-i'  

    #result = [x.to_dict() for x in db.get_many(**data)]
    #q = query.Or([{x:data[x]} for x in data])
    #pprint(q)
    #result = [x.to_dict() for x in db.get_many(**q)]
    result = [x.to_dict() for x in db.get_many()]
    for res in result:
        res["doctors"] = [x.to_dict() for x in masterdb.account.get_many(account_type="doctor", clinic=res["uid"])]

    final = []
    for res in result:

        if data["query"].lower() in res["name"].lower():
            final.append(res)
            continue

        if data["query"].lower() in res["address"].lower():
            final.append(res)
            continue

        if data["query"].lower() in res["city"].lower():
            final.append(res)
            continue

        if data["query"].lower() in res["province"].lower():
            final.append(res)
            continue

        for doc in res["doctors"]:
            if data["query"].lower() in doc["username"].lower():
                final.append(res)
                break

            if data["query"].lower() in doc["specialty"].lower():
                final.append(res)
                break


    return jsonify(final)


