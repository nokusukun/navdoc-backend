from models.master import Master



class Clinic(Master):

    properties = ["uid", "name", "city", "province", "address", "contact_number", "coordinates", "author", "active"]
    model_type = "clinic"

    def __init__(self, data=None):
        super().__init__(data)


clinic_hours = {"sun": [0, 0],
                "mon": [700, 1600],
                "tue": [900, 1600],
                "wed": [1000, 1500],
                "thu": [700, 1600],
                "fri": [0, 0],
                "sat": [800, 1100]}