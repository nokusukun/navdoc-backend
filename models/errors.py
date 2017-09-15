

class account():
    def iserror(val):
        return val in account.__dict__.values()
    e00 = ["a00", "You're not logged in."]
    e01 = ["a01", "No account type specified."]
    e02 = ["a02", "Missing required fields."]
    e03 = ["a03", "Email already exists."]
    e04 = ["a04", "Account does not exist."]
    e05 = ["a05", "Invalid password."]
    e06 = ["a06", "Invalid Credentials"]
    e07 = ["a07", "Foreign fields present."]
    e08 = ["a08", "Session-Token Error"]
    e09 = ["a09", "Doctor does not exist."]

class db():
    def iserror(val):
        return val in db.__dict__.values()
    e00 = ["db00", "Unknown database error."]
    e01 = ["db01", "Email already exists."]
    e02 = ["db02", "Username already exists."]

class clinic():
    def iserror(val):
        return val in db.__dict__.values()
    e00 = ["c00", "Clinic does not exist."]
    e01 = ["c01", "You are not the owner of this clinic."]