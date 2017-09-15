import json
import secrets
import arrow
from flask import Blueprint, render_template, abort, jsonify
from flask import Flask, send_from_directory, request, session, redirect, send_file, url_for

from models import errors
from base import utils
from functools import wraps


prefix = "/data"
db = None
com = Blueprint("data", __name__)

# Load Location Data
location_data = {}
with open("locations.txt") as f:
    locs = f.readlines()
locs = [x.replace("\n", "").split("\t") for x in locs]

for l in locs:
    if l[9] in location_data:
        location_data[l[9]].append(l[1])
    else:
        location_data[l[9]] = [l[1]]

medspec = {}

with open("med-spec.json") as f:
    medspec = json.loads(f.read())

sess = None
s_data = lambda : sess[request.headers["Session-Token"]]

def Load(_app, _db, session_data):
    global db
    db      = _db
    app     = _app
    sess = session_data
    _app.register_blueprint(com, url_prefix=prefix)


def require_login(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        print(f"[{f.__name__}] This endpoint requires to be logged in.")
        if s_data().get("uid") is None:
            abort(400, errors.account.e00)
        else:
            return f(*args, **kwargs)
    return wrap


@com.route("/locations", methods=["GET", "POST"])
@require_login
def g_locations():

    return jsonify(location_data)


@com.route("/medspec", methods=["GET", "POST"])
@require_login
def g_medspec():

    return jsonify(medspec)
