import json


# yes, this is wrong.
def is_jsonable(data):
    try:
        json.dumps(data)
        return True
    except:
        return False


class Master():

    model_type = "master"

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