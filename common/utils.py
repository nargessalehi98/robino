import re

from bson import ObjectId
from pymongo import MongoClient


def get_db_handle(db_name, host, port):
    client = MongoClient(host=host,
                         port=int(port))
    db_handle = client[db_name]
    return db_handle, client


def get_collection_handle(db_handle, collection_name):
    return db_handle[collection_name]


def object_id_convertor_to_string(id):
    return str(id)


def item_id_convertor_to_string(item):
    item['_id'] = str(item['_id'])


def item_id_convertor_to_ObjectId(item):
    item['_id'] = ObjectId(item['_id'])


def email_is_valid(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if (re.fullmatch(regex, email)):
        return True
    return False


def password_is_valid(password):
    while True:
        if len(password) < 8:
            return False
        elif re.search('[0-9]', password) is None:
            return False
        elif re.search('[A-Z]', password) is None:
            return False
        else:
            return True
