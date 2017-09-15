import hashlib
import config
from bson import json_util
import json


def jsonize(data):
    return json_util.dumps(data)

def validate(what, to):
    pass

def hash(data):
    return hashlib.sha224(f"{data}{config.SECRET_KEY}".encode()).hexdigest()

