import json
import secrets
import arrow
import requests
from flask import Blueprint, render_template, abort, jsonify
from flask import Flask, send_from_directory, request, session, redirect, send_file, url_for
from flask_cors import CORS, cross_origin

import config
from models import misc 
from models import errors
from base import utils
from functools import wraps


prefix = "/transaction"
db = None
com = Blueprint("transaction", __name__)
CORS(com)
masterdb = None

sess = None
s_data = lambda : sess[request.headers["Session-Token"]]

get_account = lambda x: requests.get(f"https://api-uat.unionbankph.com/hackathon/sb/accounts/{x}", 
                        headers={   'accept': 'application/json', 
                                    'x-ibm-client-id': config.BANK_ID, 
                                    'x-ibm-client-secret': config.BANK_SECRET
                                }).json()

# curl --request POST \
#   --url https://api-uat.unionbankph.com/hackathon/sb/transfers/initiate \
#   --header 'accept: application/json' \
#   --header 'content-type: application/json' \
#   --header 'x-ibm-client-id: REPLACE_THIS_KEY' \
#   --header 'x-ibm-client-secret: REPLACE_THIS_KEY' \
#   --data '{"channel_id":"UHAC_TEAM","transaction_id":"001","source_account":"XXXXXXXXXX1","source_currency":"PHP","target_account":"XXXXXXXXXX2","target_currency":"PHP","amount":7}'

transfer_funds = lambda uid, source, destination, ammount: requests.post(f"https://api-uat.unionbankph.com/hackathon/sb/transfers/initiate", 
                    headers={   'accept':'application/json', 
                                'content-type':'application/json',
                                'x-ibm-client-id': config.BANK_ID, 
                                'x-ibm-client-secret': config.BANK_SECRET
                            }, data=json.dumps({"channel_id": "DOCNAV",
                                                "transaction_id": uid,
                                                "source_account": source,
                                                "source_currency":"PHP",
                                                "target_account": destination,
                                                "target_currency":"PHP",
                                                "amount":ammount})).json()


def Load(_app, _db, session_data):
    global db, sess, masterdb
    db      = _db.transaction
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

    
@com.route("/create", methods=["GET", "POST"])
@require_login
def transaction_add():
    required = ["source", "amount", "description", "trans_type"]
    data = request.get_json(force=True)

    new_transaction = misc.Transaction(data)
    val = new_transaction.validate(required)
    if val:
        abort(400, errors.account.e02 + [val])

    new_transaction.uid = secrets.token_hex(8)
    new_transaction.author = s_data()["uid"]
    new_transaction.active = True
    new_transaction.status = "pending"
    print(new_transaction.to_dict())
    result = db.add(new_transaction)

    if errors.db.iserror(result):
        abort(400, result)

    new_transaction.__dict__["success"] = True
    return jsonify(new_transaction.to_dict())


@com.route("/get_appt/<apptid>")
def transactions_get(apptid):
    appointment = masterdb.appointment.get_one(uid=apptid).to_dict()
    appointment["transactions"] = db.get_many(source=apptid)
    
    return jsonify(appointment)


@com.route("/get/<tid>")
def transaction_get(tid):
    result = db.get_one(uid=tid)
    return jsonify(result.to_dict())


@com.route("/appt_ack/<apptid>")
def transactions_ack(apptid):
    result = db.get_many(source=apptid)
    print(result)
    appointment = masterdb.appointment.get_one(uid=apptid)
    doctor = masterdb.account.get_one(uid=appointment.doctor)
    user = masterdb.account.get_one(uid=appointment.user)

    final = []
    for re in [x.to_dict() for x in result]:
        print(re)
        if re["trans_type"] == "bank":
            xtra = transfer_funds(re["uid"], user.bank_no, doctor.bank_no, doctor.rate)
            db.update(misc.Transaction(re), {"extra": xtra, "status": "ackn"})
            final.append({"success": f"{re['uid']}", "data": xtra})
            continue
        
        elif re["trans_type"] == "direct":
            xtra = {"status": "paid"}
            db.update(misc.Transaction(re), {"extra": xtra, "status": "ackn"})
            final.append({"success": f"{re['uid']}", "data": xtra})
            continue

        else:
            final.append({"pending": f"{re['uid']}", "data": re})

    return jsonify(final)
