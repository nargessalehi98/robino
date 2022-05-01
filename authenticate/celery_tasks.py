from bson import ObjectId

from common.utils import get_collection_handle, get_db_handle
from config.celery import app

db_handler, mongo_client = get_db_handle('robinodemo', 'localhost', '27017')


class CeleryTasksAuth:
    @staticmethod
    @app.task
    def test(id, token):
        print("yyyyyyyyyyyyyyy")
        user_profile_handler = get_collection_handle(db_handler, "userprofile")
        user_profile_handler.find_one_and_update({"_id": id, "devices": {"$size": 3}},
                                                 {"$pop": {"devices": -1}})
        print("yyyyyyyyyyyyyyy")
        device = {
            "token": token,
            # "device": str(request.user_agent.device),
            # "os": str(request.user_agent.os),
            # "browser": str(request.user_agent.browser)
        }
        print("yyyyyyyyyyyyyyy")
        user_profile_handler.update({"_id": id},
                                    {"$addToSet": {"devices": device}})
        return True