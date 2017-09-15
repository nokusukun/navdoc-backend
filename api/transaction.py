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
                                })

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
    required = ["source", "ammount", "description"]
    data = request.get_json(force=True)

    new_transaction = misc.Transaction(data)
    val = new_transaction.validate(required)
    if val:
        abort(400, errors.account.e02 + [val])

    new_transaction.uid = secrets.token_hex(8)
    new_transaction.author = s_data()["uid"]
    new_transaction.active = True
    result = db.add(new_transaction)

    if errors.db.iserror(result):
        abort(400, result)

    new_transaction.__dict__["success"] = True
    return jsonify(new_transaction.to_dict())

