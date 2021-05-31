import ssl
import json
import pymongo
import pandas as pd
from pandas import ExcelWriter, ExcelFile

with open('.env', 'r') as f:
    env = json.load(f)

with open('data/events.json', 'r') as f:
    event_codes = []
    events = json.load(f)
    for event in events:
        event_codes.append(event['code'])

mongo_client = pymongo.MongoClient(f'mongodb+srv://{env["mongo_user"]}:{env["mongo_pass"]}@hacky-cluster.a7nnk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority', ssl_cert_reqs=ssl.CERT_NONE)
db = mongo_client['Hack^2']
db_col = db['users']


def writeData():
    df = pd.read_csv('users_data.csv')
    discord_names = df['discord_name'].dropna().to_list()
    discord_tags = df['discord_tag'].dropna().to_list()

    users = []
    for discord_name, discord_tag in zip(discord_names, discord_tags):
        discord_tag = discord_tag.replace('#','')
        query = db_col.find({'discord_name' : f'{discord_name}', 'discord_tag' : f'{discord_tag}'})
        unique = [x for x in query]
        if not unique:
            tmp = {"discord_name": f"{discord_name}", "discord_tag": f"{discord_tag}", "codes_used": [], "workshops_attended": "0" }
            db_col.insert_one(tmp)
            print('[+] Added new user to the database.')
        else:
            pass


def verifyCode(discord_name, discord_tag, code):
    query = db_col.find({'discord_name' : f'{discord_name}', 'discord_tag' : f'{discord_tag}'})
    unique = [x for x in query]
    if not unique:
        return 'User not found, Please register first.'
    else:
        if code in event_codes:
            codes_used_ = []
            codes_used = unique[0]['codes_used']
            if not codes_used:
                codes_used_.append(code)
                db_col.update({"discord_name" : f"{discord_name}", "discord_tag" : f"{discord_tag}"}, {"$set" : {"codes_used" :codes_used_, "workshops_attended" : len(codes_used_)}})
                return 'Verified code'
            else:
                if code in unique[0]['codes_used']:
                    return 'Code already redeemed.'
                else:
                    codes_used_ = unique[0]['codes_used']
                    codes_used_.append(code)
                    db_col.update({"discord_name" : f"{discord_name}", "discord_tag" : f"{discord_tag}"}, {"$set" : {"codes_used" :codes_used_, "workshops_attended" : len(codes_used_)}})
                    return 'Verified code'
        else:
            return 'Invalid code.'
