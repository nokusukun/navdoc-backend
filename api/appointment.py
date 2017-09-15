import json
import secrets
import arrow
from flask import Blueprint, render_template, abort, jsonify
from flask import Flask, send_from_directory, request, session, redirect, send_file, url_for
from flask_cors import CORS, cross_origin

from models import misc 
from models import errors
from base import utils
from functools import wraps
import arrow

prefix = "/appointment"
db = None
com = Blueprint("appointment", __name__)
CORS(com)
masterdb = None

sess = None
s_data = lambda : sess[request.headers["Session-Token"]]

def Load(_app, _db, session_data):
    global db, sess, masterdb
    db      = _db.appointment
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


@com.route("/request", methods=["GET", "POST"])
@require_login
def request_appointment():
    required = ["doctor", "date", "purpose"]
    data = request.get_json(force=True)
    doctor_data = masterdb.account.get_one(uid=data["doctor"], account_type="doctor")

    if doctor_data.uid is None:
        abort(400, errors.account.e09)

    new_appointment = misc.Appointment(data)
    val = new_appointment.validate(required)
    if val:
        abort(400, errors.account.e02 + [val])

    new_appointment.uid = secrets.token_hex(8)
    new_appointment.user = s_data()["uid"]
    new_appointment.status = "pending"
    new_appointment.active = "true"
    new_appointment.reason = ["None"]
    result = db.add(new_appointment)

    if errors.db.iserror(result):
        abort(400, result)

    new_appointment.__dict__["success"] = True
    return jsonify(new_appointment.to_dict())



@com.route("/get/<atype>", methods=["GET", "POST"])
@require_login
def get_appointment(atype):
    if s_data()["userdata"]["account_type"] == "user":
        data = db.get_many(user=s_data()["uid"], status=atype)
    else:
        data = db.get_many(doctor=s_data()["uid"], status=atype)
    print(data)
    final = []
    for d in data:
        d = d.to_dict()
        d["doctor"] = masterdb.account.get_one(uid=d["doctor"]).to_dict()
        d["doctor"]["clinic"] = masterdb.clinic.get_one(uid=d["doctor"]["clinic"]).to_dict()
        d["user"] = masterdb.account.get_one(uid=d["user"]).to_dict()
        final.append(d)

    # if not data:
    #     abort(400, ["e00", "Appointment does not exist."])

    return jsonify(final)


@com.route("/today", methods=["GET", "POST"])
@require_login
def get_appointment_today():
    date = arrow.now().timestamp
    if s_data()["userdata"]["account_type"] == "user":
        d = db.get_many(user=s_data()["uid"], date=date)
    else:
        d = db.get_many(doctor=s_data()["uid"], date=date)
    print(data)
    d = d.to_dict()
    d["doctor"] = masterdb.account.get_one(uid=d["doctor"]).to_dict()
    d["doctor"]["clinic"] = masterdb.clinic.get_one(uid=d["doctor"]["clinic"]).to_dict()
    d["user"] = masterdb.account.get_one(uid=d["user"]).to_dict()

    # if not data:
    #     abort(400, ["e00", "Appointment does not exist."])

    return jsonify(d)


@com.route("/get_single/<uid>", methods=["GET", "POST"])
@require_login
def get_appointment_solo(uid):
    d = db.get_one(uid=uid)
    print(data)
    d["doctor"] = masterdb.account.get_one(uid=d["doctor"]).to_dict()
    d["doctor"]["clinic"] = masterdb.clinic.get_one(uid=d["doctor"]["clinic"]).to_dict()
    d["user"] = masterdb.account.get_one(uid=d["user"]).to_dict()
    # if not data:
    #     abort(400, ["e00", "Appointment does not exist."])

    return jsonify(d)


@com.route("/accept/<appointment_id>", methods=["GET", "POST"])
@require_login
def accept_appointment(appointment_id):
    data = db.get_one(uid=appointment_id, status="pending")
    print(data.to_dict())
    if data.uid is None:
        abort(400, ["e00", "Appointment does not exist."])

    if data.doctor != s_data()["uid"]:
        abort(400, ["e00", "Mismatching credentials. Authorization denied."])


    result = db.update(data, {"status": "approved"})

    if result:
        return jsonify({"success": f"Appointment '{appointment_id} ' approved by doctor."})
    else:
        abort(400, ["db00", "Unknown database error."])


@com.route("/decline/<appointment_id>", methods=["GET", "POST"])
@require_login
def decline_appointment(appointment_id):
    data = db.get_one(uid=appointment_id, status="pending")
    print(data.to_dict())
    if data.uid is None:
        abort(400, ["e00", "Appointment does not exist."])

    if data.doctor != s_data()["uid"]:
        abort(400, ["e00", "Mismatching credentials. Authorization denied."])


    result = db.update(data, {"status": "declined"})

    if result:
        return jsonify({"success": f"Appointment '{appointment_id} ' approved by doctor."})
    else:
        abort(400, ["db00", "Unknown database error."])




@com.route("/update/<appointment_id>", methods=["POST"])
@require_login
def update_appointment(appointment_id):
    filters = ["uid", "status", "user", "timestamp"]
    new_data = request.get_json(force=True)
    for filt in filters:
        if filt in new_data:
            new_data.pop(filt)

    data = db.get_one(uid=appointment_id, status="pending")
    print(data.to_dict())
    if data.uid is None:
        abort(400, ["e00", "Appointment does not exist."])

    if data.doctor != s_data()["uid"]:
        abort(400, ["e00", "Mismatching credentials. Authorization denied."])

    result = db.update(data, new_data)

    if result:
        return jsonify({"success": f"Appointment '{appointment_id} ' approved by doctor."})
    else:
        abort(400, ["db00", "Unknown database error."])


@com.route("/finish/<appointment_id>", methods=["GET", "POST"])
@require_login
def finish_appointment(appointment_id):
    data = db.get_one(uid=appointment_id, status="approved")
    print(data.to_dict())
    if data.uid is None:
        abort(400, ["e00", "Appointment does not exist."])

    if data.doctor != s_data()["uid"]:
        abort(400, 
            ["e00", "Mismatching credentials. Authorization denied."])

    result = db.update(data, {"status": "done"})

    if result:
        return jsonify({"success": f"Appointment '{appointment_id} ' finished by doctor."})
    else:
        abort(400, ["db00", "Unknown database error."])



@com.route("/reschedule/<appointment_id>", methods=["POST"])
@require_login
def reschedule_appointment(appointment_id):
    new_data = request.get_json(force=True)
    data = db.get_one(uid=appointment_id, status="approved")
    print(data.to_dict())
    if data.uid is None:
        abort(400, ["e00", "Appointment does not exist."])

    data.date.append(new_data)
    result = db.update(data, {"date": data.date})

    if result:
        return jsonify({"success": f"Appointment '{appointment_id} ' finished by doctor."})
    else:
        abort(400, ["db00", "Unknown database error."])


