import pymongo
import config
import json
import secrets
import random
import requests
import config

database = pymongo.MongoClient(config.DATABASE_URI).uhack
account_names = ['Dianne Gibson',
            'Noel Klein',
            'Kristina Henry',
            'Jacquelyn Bass',
            'Audrey Peters',
            'Roberto Baker',
            'Lorraine Ortiz',
            'Woodrow Robbins',
            'Nettie Davis',
            'Jesse Wong',
            'Antoinette Simpson',
            'Leonard Lucas',
            'Scott Herrera',
            'Santos Harmon',
            'Terrance Blake',
            'Colin Hicks',
            'Sonya Banks',
            'Leland Garner',
            'Eleanor Willis',
            'Patricia Young',
            'Jodi Stone',
            'Lorene Vaughn',
            'Rachael Ingram',
            'Linda Brock',
            'Judy Barker',
            'Warren Clarke',
            'Julian Murphy',
            'Darryl Lambert',
            'Blake Fletcher',
            'Spencer Padilla',
            'Gilbert Washington',
            'Minnie Drake',
            'Willard Henderson',
            'Carl Holt',
            'Marcia Francis',
            'Stephanie May',
            'Brad Walker',
            'George Nichols',
            'Richard Pratt',
            'Veronica Lindsey',
            'Catherine Larson',
            'Bernadette Hughes',
            'Caroline Douglas',
            'Velma Powers',
            'Edna Hall',
            'Wanda Paul',
            'Phillip Ferguson',
            'Marcus Ramsey',
            'Darrel Ballard',
            'Vickie Gross',
            'Shane Peterson',
            'Norma Campbell',
            'Maggie Watts',
            'Freda Marshall',
            'Jill Sullivan',
            'Jeremy Mann',
            'Marie Graham',
            'Leona Bailey',
            'Shelia Fisher',
            'Milton Hunter',
            'Glenn Carpenter',
            'Gladys Mitchell',
            'Nicolas Curti',
            'Claudia Hill',
            'Stewart Holloway',
            'Danielle Tate',
            'Calvin Gross',
            'Victoria Erickson',
            'Deborah Gonzales',
            'Kent Vaughn',
            'Drew Gilbert',
            'Melanie Woods',
            'Rhonda Oliver',
            'Jake Sullivan',
            'Jose Harris',
            'Pearl Hammond',
            'Sally Wright',
            'Dwayne Price',
            'Bertha Willis',
            'Dominick Butler',
            'Tim Garrett',
            'Mae Cooper',
            'Antonio Carr',
            'Krista Casey',
            'Orlando Porter',
            'Wendy Baldwin',
            'Cory Rhodes',
            'Benny Russell',
            'Dominic Mann',
            'Roosevelt Walker',
            'Reginald Olson',
            'Fernando Garner',
            'Tony Thomas',
            'Lola Steele',
            'Leo Foster',
            'Gregory Gardner',
            'Patty Diaz',
            'Clara Greene',
            'Grace Padilla',
            'Frankie Torres',
            'Megan Floyd',
            'Verna Roberson',
            'Charles Reyes',
            'Freda Parker',
            'Lula Shaw',
            'Dolores Townsend',
            'Colin Norton',
            'Mona Taylor',
            'Andres Wood',
            'Nathan Nguyen',
            'Stephen Mack',
            'Ian Massey',
            'Caroline Maldonado',
            'Olivia Frazier',
            'Irving Gray',
            'Jodi Morton',
            'Marta Griffith',
            'Salvatore Klein',
            'Sergio Herrera',
            'Kelli James',
            'Leona Bush',
            'Elsie Keller',
            'Sandra Carson',
            'Nina Watts',
            'Jeanne Davis',
            'Kenneth Flowers',
            'Alexis Alvarado',
            'Jana Ellis',
            'Gerard Fitzgerald',
            'Henry Davidson',
            'Phil Lynch',
            'Micheal Bradley',
            'Jacqueline Delgado',
            'Jeannie Romero',
            'Jesus Phelps',
            'Margarita Jordan',
            'Laura Lawrence',
            'Felix Warner',
            'Maryann Bowen',
            'Marty Yates',
            'Edgar Brooks',
            'Esther Stevenson',
            'Lydia Strickland',
            'Sheri Shelton',
            'Myra Patrick',
            'Julius Thornton',
            'Geoffrey Black',
            'Daisy Wilson',
            'Marion Schultz',
            'Gordon Rodriquez',
            'Monica Maxwell',
            'Eleanor Graham',
            'Mary Perkins',
            'Wallace Stewart',
            'Travis Salazar',
            'Luther Mendez',
            'Israel Leonard',
            'Edward Blake',
            'Dallas Johnston',
            'Wendell West',
            'Randall Moreno',
            'Shannon Harmon',
            'Priscilla Curry'
        ]
names = ['Alliance',
            'Amity',
            'Angelstone',
            'Angelvale',
            'Angelwing',
            'Angelwood',
            'Animas',
            'Archangel',
            'Bayhealth',
            'Bayview',
            'Beacon',
            'Bellevue',
            'Bellflower',
            'Big Heart',
            'Big River',
            'Blessings',
            'Blossom',
            'Blossom Valley',
            'Blossomvale',
            'Broadwater',
            'Castle',
            'Charity',
            'Cherry Blossom',
            'Citrus',
            'Clearview',
            'Clearwater Lake',
            'Clearwater Valley',
            'Clemency',
            'Crossroads',
            'Desert Springs',
            'Diamond Grove',
            'East Valley',
            'Eden',
            'Edgewater',
            'Evergreen',
            'Fairbanks',
            'Fairmont',
            'Fairview',
            'Featherfall',
            'Flowerhill',
            'Forest Health',
            'Forest View',
            'Fortuna',
            'Fortune',
            'Fountain Valley',
            'Freeman',
            'Garden City',
            'Garden Grove',
            'Genesis',
            'Golden Oak',
            'Golden Valley',
            'Goldriver',
            'Goldvalley',
            'Good Samaritan',
            'Grace',
            'Grand Garden',
            'Grand Meadow',
            'Grand Mountain',
            'Grand Oak',
            'Grand Plains',
            'Grand River',
            'Grand University',
            'Grand Valley',
            'Grand View',
            'Grand Willow',
            'Grandview',
            'Great Plains',
            'Great River',
            'Green Country',
            'Green Hill',
            'Greengrass',
            'Greenlawn',
            'Greenwood',
            'Griffin',
            'Guardian',
            'Hallmark',
            'Harmony',
            'Harmony Grove',
            'Healthbridge',
            'Healthstone',
            'Heart Center',
            'Heartland',
            'Heartstone',
            'Highland',
            'Highlands',
            'Hill Crest',
            'Hillsdale',
            'Honor',
            'Honor Grave',
            'Hope Garden',
            'Hope Haven',
            'Hope Valley',
            'Hopedale',
            'Hopevale',
            'Horizon',
            'Hot Springs',
            'Hyacinth',
            'Jade Forest',
            'Kindred',
            'Kindred Soul',
            'Laguna',
            'Lakeland',
            'Lakeside',
            'Lakewood',
            'Lifecare',
            'Light Beacon',
            'Lilypad',
            'Lilypad Gardens',
            'Little River',
            'Love',
            'Lowland',
            'Lullaby',
            'Magnolia',
            'Maple Grove',
            'Maple Valley',
            'Marine',
            'Meadowview',
            'Memorial',
            'Mercy',
            'Mercy Vale',
            'Mineral',
            'Morningside',
            'Mountain View',
            'New Eden',
            'New Horizons',
            'Noble',
            'North Star',
            'Northshore',
            'Oak Crest',
            'Oak Valley',
            'Oakdale',
            'Oasis',
            'Olympus',
            'Orange Garden',
            'Overlook',
            'Paradise Grove',
            'Paradise Valley',
            'Parkview',
            'Peace Forest',
            'Peace River',
            'Peak View',
            'Pearl River',
            'Petunia',
            'Phoenix',
            'Pine Rest',
            'Pine Valley',
            'Pinevale',
            'Pinevalley',
            'Pioneer',
            'Primary',
            'Principal',
            'Progress',
            'Promise',
            'Rainbow',
            'Repose',
            'Ridgeview',
            'Riverside',
            'Riverview',
            'Rose',
            'Rose Gardens',
            'Rose Petal',
            'Rose Valley',
            'Rosemary',
            'Rosewood',
            'Ruby Valley',
            'Sacred Heart',
            'Samaritan',
            'Sapphire Lake',
            'Serenity',
            'Silver Birch',
            'Silver Boulder',
            'Silver Gardens',
            'Silver Hill',
            'Silver Lake',
            'Silver Oak',
            'Silver Pine',
            'Silver Wing',
            'Silverstone',
            'Silverwood',
            'Snowflake',
            'Southshore',
            'Specialty',
            'Spring Forest',
            'Spring Fountain',
            'Spring Grove',
            'Spring Harbor',
            'Spring Hill',
            'Spring River',
            'Springfield',
            'Springhill',
            'Stillwater',
            'Summer Springs',
            'Summerfield',
            'Summerhill',
            'Summerstone',
            'Summit',
            'Swan River',
            'Swanlake',
            'Tranquil Valley',
            'Tranquility',
            'Trinity',
            'Tulip',
            'Twin Lakes',
            'Twin Mountains',
            'Union',
            'United',
            'Valley Health',
            'Wellness',
            'West Valley',
            'Westview',
            'White Blossom',
            'White Feather',
            'White Mountain',
            'White Petal',
            'White River',
            'White Willow',
            'White Wing',
            'Wildflower',
            'Willow Gardens',
            'Woodland',
            'Clinic',
            'Community Hospital',
            'General Hospital',
            'Hospital',
            'Hospital Center',
            'Medical Center',
            'Medical Clinic'
        ]

with open("users.json") as f:
    users = json.loads(f.read())

with open("doctorsample.json") as f:
    doctors = json.loads(f.read())

def gen_bday():
    month = random.choice(range(1, 12))
    day = random.choice(range(1, 30))
    year = random.choice(range(1980, 1998))


def gen_coord():
     a = lambda : random.choice(range(6873454965, 7362598229))
     b = lambda : random.choice(range(5226211547, 5797843933))
     return [float(f"10.{a()}"), float(f"122.{b()}")]


def gen_hours():
    r = list(range(7, 12))
    t = list(range(13, 18))
    a = lambda x: random.choice(x)
    data = {"sun": [int(f"{a(r)}00"), int(f"{a(t)}00")],
            "mon": [int(f"{a(r)}00"), int(f"{a(t)}00")],
            "tue": [int(f"{a(r)}00"), int(f"{a(t)}00")],
            "wed": [int(f"{a(r)}00"), int(f"{a(t)}00")],
            "thu": [int(f"{a(r)}00"), int(f"{a(t)}00")],
            "fri": [int(f"{a(r)}00"), int(f"{a(t)}00")],
            "sat": [int(f"{a(r)}00"), int(f"{a(t)}00")]}
    return data



# 
# curl --request POST \
#   --url https://api-uat.unionbankph.com/hackathon/sb/test/accounts \
#   --header 'accept: application/json' \
#   --header 'content-type: application/json' \
#   --header 'x-ibm-client-id: REPLACE_THIS_KEY' \
#   --header 'x-ibm-client-secret: REPLACE_THIS_KEY' \
#   --data '{"accountName":"sample string 1"}'
# 

request_account = lambda x: requests.post(f"https://api-uat.unionbankph.com/hackathon/sb/test/accounts", 
                    headers={   'accept':'application/json', 
                                'content-type':'application/json',
                                'x-ibm-client-id': config.BANK_ID, 
                                'x-ibm-client-secret': config.BANK_SECRET
                            }, data=json.dumps({"accountName": x})).json()

usr_bank = request_account("user-savings")
doc_bank = request_account("docs-bank")
database.account.drop()
database.clinic.drop()

for usr in users:
    usr["uid"] = secrets.token_hex(8)
    usr["gender"] = random.choice(["male", "female"])
    usr["birthday"] = gen_bday()
    usr["bank_no"] = usr_bank[0]["account_no"]
    print(f"Inserting user: {usr['uid']}")
    database.account.insert(usr)

usr = {}
usr["uid"] = secrets.token_hex(8)
usr["account_type"] = "admin"
usr["email"] = "admin@admin"
usr["username"] = "Administrator Castrator"
usr["password"] = "password"
database.account.insert(usr)

# Clinic
clinics = []
for i in range(0,100):
    # "uid", "name", "city", "province", "address", "contact_number", "coordinates", "author", "active"
    coordinates = gen_coord()
    data = {"uid": secrets.token_hex(8),
            "name": f"{random.choice(names)} {random.choice(names)}",
            "city": "Iloilo",
            "province": "Iloilo",
            "address": f"{random.choice(range(1, 30))} {random.choice(names)} St. {random.choice(names)}",
            "contact_number": f"+639{random.choice(range(10000000, 99999999))}",
            "coordinates": {
                    "lat": coordinates[0],
                    "lng": coordinates[1]
                    },
            "author": "aaaaaaaa",
            "active": True
            }
    print(f"Inserting clinic: {data['uid']}")
    clinics.append(data['uid'])
    database.clinic.insert(data)


first_name = [x.split(" ")[0] for x in account_names]
last_name = [x.split(" ")[-1] for x in account_names]

med_spec = [
        "Anaesthesiology",
        "None",
        "Aerospace medicine",
        "Pathology",
        "Dermatology-Venereology",
        "General practice",
        "Obstetrics and gynaecology",
        "Health informatics",
        "Internal medicine",
        "Microbiology",
        "Nuclear medicine",
        "Occupational medicine",
        "Ophthalmology",
        "Orthodontics",
        "Otorhinolaryngology",
        "Paediatrics",
        "Physical medicine and rehabilitation",
        "Public Health",
        "Radiation Oncology",
        "Radiology",
        "General surgery"
    ]

for i in range(10, 300):
    # ["hours", "pma", "field", "specialty", "prc", "prc_id", "clinic", "affiliation", "max_patients", "online", "validated"]
    usr = {}
    usr["uid"] = secrets.token_hex(10)
    usr["email"] = f"test{i}@gmail.com"
    usr["password"] = "password"
    usr["account_type"] = "doctor"
    usr["gender"] = random.choice(["male", "female"])
    usr["birthday"] = gen_bday()
    usr["username"] = f"{random.choice(first_name)} {random.choice(last_name)}"
    usr["clinic"] = random.choice(clinics)
    usr["hours"] = gen_hours()
    usr["rate"] = random.choice(range(200, 500))
    #09990-00099-999
    usr["pma"] = f"{random.choice(range(10000, 99999))}-{random.choice(range(10000, 99999))}-{random.choice(range(100, 999))}"
    usr["field"] = random.choice(med_spec)
    usr["specialty"] = usr["field"]
    usr["max_patients"] = random.choice(range(30, 80))
    usr["validated"] = random.choice([True, True, True, False])
    usr["online"] = random.choice([True, True, True, False])
    usr["active"] = True
    usr["bank_no"] = doc_bank[0]["account_no"]

    print(f"Inserting doctor: {usr['uid']}")
    database.account.insert(usr)

print(doc_bank)
print(usr_bank)
