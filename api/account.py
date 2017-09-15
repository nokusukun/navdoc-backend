import json
import secrets
import arrow
from pprint import pprint
from flask import Blueprint, render_template, abort, jsonify, Response
from flask import Flask, send_from_directory, request, session, redirect, send_file, url_for
from flask_cors import CORS, cross_origin

from models import account
from models import errors
from base import utils
from base import QueryOp as query
from functools import wraps


prefix = "/account"
db = None
com = Blueprint("account", __name__)
CORS(com)
masterdb = None

sess = None
s_data = lambda : sess[request.headers["Session-Token"]]

def Load(_app, _db, session_data):
    global db, sess, masterdb
    db      = _db.account
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

def require_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        print(f"[{f.__name__}] This endpoint requires administrator permissions.")
        if s_data()["userdata"]["account_type"] != "admin":
            abort(400, ["e00", "Access Denied"])
        return f
    return wrap



# Delete on production
@com.route("/delete_all")
def account_delete():
    db.collection.drop()
    try:
        account_logout()
    except:
        pass
    return jsonify({"Success": "RIP Database"})


@com.route("/me", methods=["GET", "POST"])
@require_login
def account_me():
    token = request.headers["Session-Token"]
    print(sess[token].get("uid"))
    #if not session.get("userdata"):
    sess[token]["userdata"] = db.get_one(uid=sess[token]["uid"]).to_dict()
    sess[token]["userdata"]["success"] = True
    return jsonify(s_data()["userdata"])



@com.route("/logout", methods=["GET", "POST"])
@com.route("/logout/<session_token>", methods=["GET", "POST"])
def account_logout(token=None):
    try:
        if token:
            sess[token].pop("uid")
            sess[token].pop("userdata")
        else:
            s_data().pop("uid")
            s_data().pop("userdata")
    except:
        pass

    return jsonify({"success": "You have been logged out. I think."})


@com.route("/login", methods=["POST"])
def account_login():
    data = request.get_json(force=True)
    pprint(data)
    account = db.get_one(email=data["email"])
    if not account.uid:
        abort(400, errors.account.e04)

    #if utils.hash(data["password"]) == account.password:
    print(account.password)
    if data["password"] == account.password:
        session_token = secrets.token_hex(32)
        sess[session_token] = {}
        sess[session_token]["uid"] = account.uid
        sess[session_token]["userdata"] = account.to_dict()
        #return jsonify({"success": account.uid})
        
        return jsonify({"session_token": session_token})
    else:
        abort(400, errors.account.e05)


@com.route("/register", methods=["POST"])
def g_account_register():
    required = ["username", "password", "email"]
    data = request.get_json(force=True)
    try:
        data.pop("repassword")
    except:
        pass
    print("Login Process")
    if not data.get("account_type") or data.get("account_type") not in ["doctor", "user"]:
        abort(400, errors.account.e01)

    if data["account_type"] == "user":
        new_account = account.User(data)
    else:
        new_account = account.Doctor(data)
        new_account.validated = False

    val = new_account.validate(required)
    if val:
        abort(400, errors.account.e02 + [val])

    new_account.uid = secrets.token_hex(8)
    new_account.join_date = arrow.utcnow().timestamp
    new_account.active = True
    #new_account.password = utils.hash(new_account.password)

    result = db.register(new_account)

    if errors.db.iserror(result):
        abort(400, result)

    session_token = secrets.token_hex(32)
    sess[session_token] = {}
    sess[session_token]["uid"] = result.uid
    sess[session_token]["userdata"] = result.to_dict()
    pprint(result.to_dict())

    print(f"Login Process: {result.uid}")
    resp = Response(json.dumps({"session_token": session_token}))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.content_type = "application/json"
    return resp


@com.route("/update", methods=["POST"])
def account_modify():
    data = request.get_json(force=True)

    restricted_types = ["username", "email", "password", "account_type", "active"]
    for r_type in restricted_types: 
        if r_type in data: 
            data.pop(r_type)

    account_data = db.get_one(uid=session["uid"])
    pprint(account_data.to_dict())
    result = db.update(account_data, data)
    if result is None:
        abort(400, errors.account.e07)

    return jsonify(account_data.to_dict())


@com.route("/doctors/search", methods=["POST"])
def doctors_search():
    data = request.get_json(force=True)
    for key in data:
        data[key] = query.Regex(f".*{data[key]}.*")
        data[key]["$options"] = '-i'  

    #result = [x.to_dict() for x in db.get_many(**data)]
    q = query.Or([{x:data[x]} for x in data])
    pprint(q)
    result = [x.to_dict() for x in db.get_many(**q)]

    return jsonify(result)


@com.route("/doctors/get/<uid>", methods=["GET", "POST"])
def doctors_get(uid):
    
    result = db.get_one(uid=uid)
    if result.uid == None:
        abort(400, errors.account.e04)

    return jsonify(result.to_dict())



@com.route("/doctors/ratings/<uid>", methods=["GET", "POST"])
def doctors_ratings(uid):

    result = masterdb.appointment.get_many(doctor=uid)
    if not result[0].uid:
        return jsonify([])

    result = [{"rating": x["rating"], "feedback": x["feedback"]} for x in result]

    return jsonify(result)


@com.route("/doctors/unvalidated", methods=["GET", "POST"])
@require_admin
@require_login
def doctors_fetch_unvalidated():
    result = db.get_many(validated=False)
    return jsonify(result)


@com.route("/doctors/approve/<uid>", methods=["GET", "POST"])
@require_admin
@require_login
def doctors_approve(uid):

    result = db.get_one(uid=uid)
    if result.uid == None:
        abort(400, errors.account.e04)

    db.update(result, {"validated": True})
    return jsonify(result.to_dict())