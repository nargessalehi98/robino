from config.celery import app
from .inverted_index import pre_processing


class CeleryTasksSearch:
    @staticmethod
    @app.task
    def pre_processing_token(query, _id):
        pre_processing(query, _id)
        return True
