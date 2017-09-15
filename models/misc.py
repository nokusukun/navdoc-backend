import json
import arrow
from models.master import Master


class Appointment(Master):

    properties = ["uid", "status", "user", "patient_info", "doctor", "date", "appt_type", "address", "remarks", "prescription", "timestamp", "rating", "feedback"]
    # available statuses: [pending, approved, done]
    # appt_type: [clinic, house]
    model_type = "appointment"

    def __init__(self, data=None):
        super().__init__(data)
        timestamp = arrow.utcnow().timestamp


class Transaction(Master):

    properties = ["uid", "source", "ammount", "description", "timestamp"]
    model_type = "transaction"

    def __init__(self, data=None):
        super().__init__(data)
        timestamp = arrow.utcnow().timestamp
