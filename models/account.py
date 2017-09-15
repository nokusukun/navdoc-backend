import json
from models.master import Master


# yes, this is wrong.
def is_jsonable(data):
    try:
        json.dumps(data)
        return True
    except:
        return False

class Account(Master):

    properties = ["uid", "username", "password", "join_date", "active", "account_type", "email", "bank_no"]
    model_type = "account"

    def __init__(self, data=None):

        for prop in self.properties:
            self.__dict__[prop] = None

        if data:
            if "_id" in data: 
                data.pop("_id")
            if "to_dict" in data.__dir__():
                self.__dict__.update(data.to_dict())
            else: 
                self.__dict__.update(data)


    def __str__(self):
        return str(self.__dict__)


    def to_dict(self):
        for k in self.__dict__:
            if not is_jsonable(self.__dict__[k]):
                print(f"Stringifying: {k} : {self.__dict__[k]}")
                self.__dict__[k] = str(self.__dict__[k])

        return self.__dict__


    def to_json(self):
        return json.dumps(self.__dict__)

    def validate(self, check):
        # Checks if there's fields in validate that does not have any data in it.
        return [x for x in self.properties if self.__dict__.get(x) is None and x in check]


class User(Account):

    model_type = "user"

    def __init__(self, data=None):
        super().__init__(data)
        self.properties.extend(["phone_number", "birthday", "gender", "last_saved_location"])


class Doctor(Account):

    model_type = "doctor"

    def __init__(self, data=None):
        super().__init__(data)
        self.properties.extend(["hours", "pma", "field", "specialty", "prc", "prc_id", "clinic", "affiliation", "max_patients", "online", "validated"])
