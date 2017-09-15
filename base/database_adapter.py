import pymongo
import secrets
import models
from models import errors
from base import QueryOp as query


class DBModel():

    def __init__(self, m_db):
        self.collection = getattr(m_db, self.c_name)
        print(f"Initalized {self.c_name} Collection: {self.collection}")

    def add(self, data):
        if isinstance(data, self.c_model):
            return self.collection.insert_one(data.to_dict())
        else:
            raise Exception("Data passed is not a {self.c_model} model.")

    def add_many(self, data):
        try:
            compiled = [x.to_dict for x in data]
            return self.collection.insert_many(compiled)
        except AttributeError:
            raise Exception("Data passed is not a {self.c_model} model.")


    def update(self, source, data):
        new_data = {a: data[a] for a in data.keys() if source.__dict__[a] != data[a] and a in data}
        return self.collection.update_one({"uid": source.uid}, {"$set": new_data})


    def get_id(self, uid):
        return self.c_model(self.collection.find_one({"uid": uid}))


    def get_one(self, **kwarg):
        return self.c_model(self.collection.find_one(kwarg))


    def get_many(self, **kwarg):
        return [self.c_model(x) for x in self.collection.find(kwarg)]


    @property
    def size(self):
        return self.collection.count()



class DBAccount(DBModel):

    def __init__(self, m_db):
        self.c_name = "account"
        self.c_model = models.account.Account

        super().__init__(m_db)

    def register(self, account):
        # try:
        x = self.get_one(email=account.email)
        print(x)
        if x.email is not None:
            return errors.db.e01
        else:
            self.add(account)
            return account
        # except:
        #     return errors.db.e0


class DBClinic(DBModel):

    def __init__(self, m_db):
        self.c_name = "clinic"
        self.c_model = models.clinic.Clinic
        super().__init__(m_db)


class DBAppointment(DBModel):

    def __init__(self, m_db):
        self.c_name = "appointment"
        self.c_model = models.misc.Appointment
        super().__init__(m_db)


class DBTransaction(DBModel):

    def __init__(self, m_db):
        self.c_name = "transaction"
        self.c_model = models.misc.Transaction
        super().__init__(m_db)