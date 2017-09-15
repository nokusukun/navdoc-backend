from flask import Flask, render_template, send_from_directory, abort, request, session, redirect, send_file, url_for, jsonify
import flask
from flask_cors import CORS
import secrets
import json
import pymongo
import config

from dotmap import DotMap

app = Flask(__name__, static_url_path='')
app.secret_key = config.SECRET_KEY

database = pymongo.MongoClient(config.DATABASE_URI).uhack
session_server = {}

cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.errorhandler(404)
def e_404(e):
    return jsonify({"error":  "Requested resource does not exist."})


@app.errorhandler(400)
def e_400(e):
    return jsonify({"error":  e.description})

@app.route("/")
def index():
    return jsonify({"info": "navdoc-backend portal, wtf are you doing here?"})



app.run(host='192.168.43.126', port=2162, debug=True, threaded=True)