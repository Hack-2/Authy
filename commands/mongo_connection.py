import ssl
import pymongo
import settings

# Estabilish connection with mongodb.
def connect():
    mongo_client = pymongo.MongoClient(f'mongodb+srv://{settings.mongodb_user}:{settings.mongodb_pass}@hacky-cluster.a7nnk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority', ssl_cert_reqs=ssl.CERT_NONE)
    db = mongo_client['Hack^2']
    return db
