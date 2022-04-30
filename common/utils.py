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
