from bson import ObjectId
from rest_framework import serializers
from core.celery_tasks import CeleryTasksRobino
from common.messages import *
from core.serializer import db_handler
from common.utils import get_collection_handle
from common.utils import item_id_convertor_to_string


class FollowUnFollowSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True, max_length=24, min_length=24)
    profile_id = serializers.CharField(required=True, max_length=24, min_length=24)
    followings_handler = get_collection_handle(db_handler, "followings")
    followers_handler = get_collection_handle(db_handler, "followers")
    request_handler = get_collection_handle(db_handler, "requests")

    def add(self, validated_data):
        profile_id = validated_data["profile_id"]
        user_id = validated_data["user_id"]
        self.request_handler.insert_one({"requester": user_id, "receiver": profile_id})
        return {"messsage": follow_request_added}

    def create(self, validated_data):
        profile_id = validated_data["profile_id"]
        user_id = validated_data["user_id"]
        if self.followings_handler.find_one_and_delete({"user_id": user_id, "following": profile_id}):
            self.followers_handler.delete_one({"user_id": profile_id, "follower": user_id})
            CeleryTasksRobino.delete_following_posts.delay(user_id, profile_id)
            return {"message": user_unfollowed}
        else:
            self.followings_handler.insert_one({"user_id": user_id, "following": profile_id})
            self.followers_handler.insert_one({"user_id": profile_id, "follower": user_id})
            CeleryTasksRobino.update_following_posts.delay(user_id, profile_id)
        return {"message": user_followed}


class GetRequestSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True, max_length=24, min_length=24)
    request_handler = get_collection_handle(db_handler, "requests")

    def get(self, validated_data):
        requests = list(self.request_handler.find({"receiver": validated_data["user_id"]}).sort("_id", -1).limit(1))
        for request in requests:
            item_id_convertor_to_string(request)
        return {"message": requests}


class AcceptRequestSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True, max_length=24, min_length=24)
    request_id = serializers.CharField(required=True, max_length=24, min_length=24)
    request_handler = get_collection_handle(db_handler, 'requests')
    followings_handler = get_collection_handle(db_handler, "followings")
    followers_handler = get_collection_handle(db_handler, "followers")

    def get(self, validated_data):
        user_id = validated_data["user_id"]
        profile_id = list(self.request_handler.find({"_id": ObjectId(validated_data["request_id"])},
                                                    {"requester": 1}))[0]["requester"]
        self.followings_handler.insert_one({"user_id": user_id, "following": profile_id})
        self.followers_handler.insert_one({"user_id": profile_id, "follower": user_id})
        CeleryTasksRobino.update_following_posts.delay(user_id, profile_id)
        self.request_handler.remove({"_id": ObjectId(validated_data["request_id"])})
        return {"message": "TRUE"}
