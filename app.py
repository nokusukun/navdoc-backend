from flask import Flask, render_template, send_from_directory, abort, request, session, redirect, send_file, url_for, jsonify
import flask
from flask_cors import CORS
import secrets
import json
import pymongo
import config
from api import account, data, clinic, appointment, transaction
from base import database_adapter as dba
from dotmap import DotMap

app = Flask(__name__, static_url_path='')
app.secret_key = config.SECRET_KEY

database = pymongo.MongoClient(config.DATABASE_URI).uhack
session_server = {}

cors = CORS(app, resources={r"/*": {"origins": "*"}})
db_file = DotMap({})
db_file.account = dba.DBAccount(database)
db_file.clinic = dba.DBClinic(database)
db_file.appointment = dba.DBAppointment(database)
db_file.transaction = dba.DBTransaction(database)

###################################
#   view types gets loaded here   #
###################################
account.Load(app, db_file, session_server)
data.Load(app, None, session_server)
clinic.Load(app, db_file, session_server)
appointment.Load(app, db_file, session_server)
transaction.Load(app, db_file, session_server)


@app.errorhandler(404)
def e_404(e):
    return jsonify({"error":  "Requested resource does not exist."})


@app.errorhandler(400)
def e_400(e):
    return jsonify({"error":  e.description})



app.run(host='10.10.10.72', port=2162, debug=True, threaded=True)