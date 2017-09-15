import json
import arrow
from models.master import Master


class Appointment(Master):

    properties = ["uid", "status", "user", 
        "patient_info", "doctor", "date", "reason", 
        "address", "remarks", "prescription", 
        "timestamp", "rating", "feedback",
        "purpose", "active", "trans_type"]
    # available statuses: [pending, approved, declined, done]
    # appt_type: [clinic, house]
    model_type = "appointment"

    def __init__(self, data=None):
        super().__init__(data)
        timestamp = arrow.utcnow().timestamp


class Transaction(Master):

    properties = ["uid", "source", "amount", "description", "timestamp", "trans_type", "status", "extra"]
    model_type = "transaction"

    def __init__(self, data=None):
        super().__init__(data)
        timestamp = arrow.utcnow().timestamp
