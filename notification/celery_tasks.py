from bson import ObjectId
from common.utils import get_collection_handle, get_db_handle
from config.celery import app

db_handler, mongo_client = get_db_handle('robinodemo', 'localhost', '27017')
notification_handler = get_collection_handle(db_handler, 'notifications')


class CeleryTasksNotif:
    @staticmethod
    @app.task
    def add_notif_for_follow_request(object_id, user_id, from_id):
        notification_handler.insert({"user_id": user_id, "type": "request", "from": from_id, "object": object_id})
        return True

    @staticmethod
    @app.task
    def add_notif_for_like_post(object_id, user_id, from_id):
        notification_handler.insert({"user_id": user_id, "type": "like", "from": from_id, "object_id": object_id})
        return True

    @staticmethod
    @app.task
    def add_notif_for_add_comment(object_id, user_id, from_id):
        notification_handler.insert({"user_id": user_id, "type": "comment", "from": from_id, "object_id": object_id})
        return True
