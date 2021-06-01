import ssl
import json
import pymongo


with open('.env', 'r') as f:
    env = json.load(f)


mongo_client = pymongo.MongoClient(f'mongodb+srv://{env["mongo_user"]}:{env["mongo_pass"]}@hacky-cluster.a7nnk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority', ssl_cert_reqs=ssl.CERT_NONE)
db = mongo_client['Hack^2']
db_col = db['users']

db_col_events = db['events']
event_codes = [x['code'] for x in db_col_events.find()]

def verifyCode(discord_name, discord_tag, code):
    query = db_col.find({'discord_name' : f'{discord_name}', 'discord_tag' : f'{discord_tag}'})
    unique = [x for x in query]
    if not unique:
        return 'User not found, Please register first.'
    else:
        if code in event_codes:
            _codes_used = []
            codes_used = unique[0]['codes_used']
            if not codes_used:
                _codes_used.append(code)
                db_col.update({"discord_name" : f"{discord_name}", "discord_tag" : f"{discord_tag}"}, {"$set" : {"codes_used" : _codes_used, "workshops_attended" : len(_codes_used)}})
                return 'Verified code'
            else:
                if code not in unique[0]['codes_used']:
                    _codes_used = unique[0]['codes_used']
                    _codes_used.append(code)
                    db_col.update({"discord_name" : f"{discord_name}", "discord_tag" : f"{discord_tag}"}, {"$set" : {"codes_used" :_codes_used, "workshops_attended" : len(_codes_used)}})
                    return 'Verified code'
                else:
                    return 'Code already redeemed.'
        else:
            return 'Invalid code.'
