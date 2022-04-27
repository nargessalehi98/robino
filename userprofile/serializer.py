from bson import ObjectId
from rest_framework import serializers

from common.messages import post_added
from robinodemo.celery_tasks import CeleryTasksRobino
from robinodemo.serializer import db_handler
from robinodemo.utils import get_collection_handle, item_id_convertor_to_string
from search.celery_tasks import CeleryTasksSearch


class UserProfileSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True, max_length=24, min_length=24)
    _id = serializers.CharField(allow_blank=True, max_length=24)
    follower_handler = get_collection_handle(db_handler, 'followers')
    followings_handler = get_collection_handle(db_handler, 'followings')
    post_handler = get_collection_handle(db_handler, 'post')

    def get(self, validated_data, page):
        follower = self.follower_handler.find({"user_id": validated_data["user_id"]}).count()
        followings = self.followings_handler.find({"user_id": validated_data["user_id"]}).count()
        posts = self.post_handler.find({"user.id": validated_data["user_id"]}).count()
        profile_info = {}
        if page == 1:
            post_list = list(self.post_handler.find({"user.id": str(validated_data["user_id"])},
                                                    {"content": 1, "user": 1}).sort("_id", -1).limit(1))
            profile_info = {
                "followers": follower,
                "followings": followings,
                "posts": posts
            }
        else:
            post_list = list(self.post_handler.find({"user.id": str(validated_data["user_id"]),
                                                     "_id": {"$lt": ObjectId(validated_data['_id'])}},
                                                    {"content": 1, "user": 1}).sort("_id", -1).limit(1))
        for item in post_list:
            item_id_convertor_to_string(item)
        return {"message": post_list, "profile_info": profile_info}


class FollowersSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True, max_length=24, min_length=24)
    _id = serializers.CharField(allow_blank=True, max_length=24)
    follower_handler = get_collection_handle(db_handler, 'followers')
    followings_handler = get_collection_handle(db_handler, 'followings')

    def get_follower(self, validated_data, page):
        if page == 1:
            followers = list(
                self.follower_handler.find({"user_id": validated_data["user_id"]}).sort("_id", -1).limit(1))
        else:
            followers = list(
                self.follower_handler.find({"user_id": validated_data["user_id"],
                                            "_id": {"$lt": ObjectId(validated_data["_id"])}}).sort("_id", -1).limit(1))

        for item in followers:
            item_id_convertor_to_string(item)
        return {"message": followers}

    def get_following(self, validated_data, page):
        if page == 1:
            followings = list(
                self.followings_handler.find({"user_id": validated_data["user_id"]}).sort("_id", -1).limit(1))
        else:
            followings = list(
                self.followings_handler.find({"user_id": validated_data["user_id"],
                                            "_id": {"$lt": ObjectId(validated_data["_id"])}}).sort("_id", -1).limit(1))

        for item in followings:
            item_id_convertor_to_string(item)
        return {"message": followings}


class PostSerializer(serializers.Serializer):
    user = serializers.CharField(required=True, max_length=24, min_length=24)
    content = serializers.CharField(required=True, allow_null=False, max_length=280)

    def create(self, validated_data):
        user_handler = get_collection_handle(db_handler, 'userprofile')
        post_handler = get_collection_handle(db_handler, 'post')

        user_id = validated_data["user"]
        validated_data["user"] = user_handler.find_one({"_id": ObjectId(validated_data["user"])},
                                                       {"_id": 0, "username": 1, "email": 1})
        validated_data["user"]["id"] = user_id
        post = post_handler.insert_one(validated_data)
        validated_data['_id'] = str(validated_data['_id'])
        validated_data['user'] = validated_data['user']['id']

        CeleryTasksRobino.update_followers_posts.delay(user_id, validated_data)
        CeleryTasksSearch.pre_processing_token(validated_data["content"], post.inserted_id)

        return {"message": post_added}