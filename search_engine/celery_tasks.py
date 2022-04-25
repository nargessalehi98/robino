from bson import ObjectId
from pythonproject.celery import app
from robinodemo.serializer import db_handler
from robinodemo.utils import get_collection_handle
from .inverted_index import pre_processing


class CeleryTasksSearch:
    @staticmethod
    @app.task
    def pre_processing_token(query, _id):
        pre_processing(query, _id)
        return True
