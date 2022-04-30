from bson import ObjectId
from rest_framework import serializers
from common.utils import get_db_handle, get_collection_handle, item_id_convertor_to_string

db_handler, mongo_client = get_db_handle('robinodemo', 'localhost', '27017')
from common.messages import *
from .celery_tasks import CeleryTasksRobino


class UserHomeSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True, max_length=24, min_length=24)

    def get(self, validated_data, page):
        user_profile_handler = get_collection_handle(db_handler, "userprofile")
        posts = list(user_profile_handler.find({"_id": ObjectId(validated_data["user_id"])},
                                               {"new_posts": {"$slice": [page - 1, 1]}, "_id": 0, "password": 0,
                                                "email": 0, "username": 0}))[0]['new_posts']
        for item in posts:
            # en chi bud !!!!!!!!!!!!
            # item["username"] = list(user_profile_handler.find({"_id": ObjectId(item["user"])}, {"username": 1}))[0][
            #     'username']
            item_id_convertor_to_string(item)
        return {"message": posts}


# ----------------doooooooooooooooooo----------------
class ProfileSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    user_profile_handler = get_collection_handle(db_handler, 'userprofile')
    follower_handler = get_collection_handle(db_handler, 'followers')
    followings_handler = get_collection_handle(db_handler, 'followings')
    post_handler = get_collection_handle(db_handler, 'post')

    def get(self, validated_data, page):
        follower = self.follower_handler.find({"user_id": validated_data["user_id"]}).count()
        followings = self.followings_handler.find({"user_id": validated_data["user_id"]}).count()
        posts_number = self.post_handler.find({"user.id": validated_data["user_id"]}).count()
        profile_info = {
            "followers": follower,
            "followings": followings,
            "posts": posts_number
        }
        user = self.user_profile_handler.find({"username": validated_data["username"], "public": "True"})
        if user.count() == 1:
            if page == 1:
                posts = list(self.post_handler({"user.id": user.object_id}))
                for post in posts:
                    item_id_convertor_to_string(post)
                return {"messages": posts, "profile_info": profile_info}
        return {"messages": "no post"}
        # elif self.user_profile_handler.find_one({"username": validated_data["profile_user_name"]})
        # else:
        #     return {"message": user_not_found}


# ----------------done----------------
class CommentSerializer(serializers.Serializer):
    content = serializers.CharField(required=True, allow_null=False, max_length=280)
    writer = serializers.CharField(required=True, max_length=24, min_length=24)
    post_id = serializers.CharField(required=True, max_length=24, min_length=24)
    replies = serializers.IntegerField(required=True)

    def create(self, validated_data):
        # user handler
        user_handler = get_collection_handle(db_handler, 'userprofile')
        id = validated_data["writer"]
        validated_data["writer"] = user_handler.find_one({"_id": ObjectId(validated_data["writer"])},
                                                         {"_id": 0, "username": 1, "email": 1})
        validated_data["writer"]["id"] = id
        # comment handler
        comment_handler = get_collection_handle(db_handler, 'comment')
        # insert comment based on validate_data
        comment_handler.insert_one(validated_data)
        return {"message": comment_added}


# ----------------done----------------
class ReplySerializer(serializers.Serializer):
    content = serializers.CharField(required=True, allow_null=False, max_length=280)
    writer = serializers.CharField(required=True, max_length=24, min_length=24)
    post_id = serializers.CharField(required=True, max_length=24, min_length=24)
    source_id = serializers.CharField(required=True, max_length=24, min_length=24)

    def create(self, validated_data):
        # user handler
        user_handler = get_collection_handle(db_handler, 'userprofile')
        id = validated_data["writer"]
        validated_data["writer"] = user_handler.find_one({"_id": ObjectId(validated_data["writer"])},
                                                         {"_id": 0, "username": 1, "email": 1})
        validated_data["writer"]["id"] = id
        # comment handler
        comment_handler = get_collection_handle(db_handler, 'comment')
        # increase post replies
        comment_handler.update_one({"_id": ObjectId(validated_data["source_id"])}, {"$inc": {"replies": 1}})
        # insert comment based on validate_data
        comment_handler.insert_one(validated_data)
        return {"message": comment_added}


# ----------------done----------------
class LikeSerializer(serializers.Serializer):
    post_id = serializers.CharField(required=True, max_length=24, min_length=24)
    liker = serializers.CharField(required=True, max_length=24, min_length=24)

    def create(self, validated_data):
        like_handler = get_collection_handle(db_handler, 'like')
        user_handler = get_collection_handle(db_handler, 'userprofile')
        id = validated_data["liker"]
        validated_data["liker"] = user_handler.find_one({"_id": ObjectId(validated_data["liker"])},
                                                        {"_id": 0, "username": 1, "email": 1})
        validated_data["liker"]["id"] = id
        if not like_handler.find_one({"post_id": validated_data['post_id'], "liker.id": id}):
            like_handler.insert_one(validated_data)
            return {"message": "Successfully liked!"}
        return {"message": "Successfully liked before!"}


# ----------------done----------------
class PostLikingUsersSerializer(serializers.Serializer):
    post_id = serializers.CharField(required=True, max_length=24, min_length=24)
    _id = serializers.CharField(allow_blank=True, max_length=24, min_length=24)

    def get(self, validated_data, page):
        like_handler = get_collection_handle(db_handler, "like")
        if page == 1:
            likers = list(
                like_handler.find({"post_id": str(validated_data["post_id"])}, {"_id": 1, "liker": 1}).sort("_id",
                                                                                                            -1).limit(
                    1))
        else:
            likers = list(like_handler.find({"post_id": str(validated_data["post_id"]),
                                             "_id": {"$lt": ObjectId(validated_data["_id"])}},
                                            {"_id": 1, "liker": 1}).sort("_id", -1).limit(1))
        for item in likers:
            item_id_convertor_to_string(item)
        return {"message": likers}


# ----------------done----------------
class ShowCommentSerializer(serializers.Serializer):
    _id = serializers.CharField(allow_blank=True, max_length=24, min_length=24)
    post_id = serializers.CharField(required=True, max_length=24, min_length=24)

    def get(self, validated_data, page):
        comment_handler = get_collection_handle(db_handler, "comment")
        if page == 1:
            comments = list(comment_handler.find({"post_id": str(validated_data["post_id"]),
                                                  "source_id": {"$exists": False}},
                                                 {"post_id": 0}).sort("_id", -1).limit(1))

        else:
            comments = list(comment_handler.find({"post_id": str(validated_data["post_id"]),
                                                  "source_id": {"$exists": False},
                                                  "_id": {"$lt": ObjectId(validated_data["_id"])}},
                                                 {"post_id": 0}).sort("_id", -1).limit(1))

        for item in comments:
            item['_id'] = str(item['_id'])
        return {"message": comments}


# ----------------done----------------
class ShowRepliesSerializer(serializers.Serializer):
    post_id = serializers.CharField(required=True, max_length=24, min_length=24)
    comment_id = serializers.CharField(required=True, max_length=24, min_length=24)

    def get(self, validated_data, page):
        comment_handler = get_collection_handle(db_handler, "comment")
        if page == 1:
            comments = list(
                comment_handler.find({"source_id": validated_data["comment_id"]}).sort("_id", -1).limit(1))

        else:
            comments = list(comment_handler.find({"source_id": str(validated_data["comment_id"]),
                                                  "_id": {"$lt": ObjectId(validated_data["_id"])}}).sort("_id",
                                                                                                         -1).limit(1))
        for item in comments:
            item['_id'] = str(item['_id'])
        return {"message": comments}


# ----------------done----------------
class FollowersSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True, max_length=24, min_length=24)
    follower_handler = get_collection_handle(db_handler, "followers")

    def get(self, validated_data, page):
        if page == 1:
            followers = list(self.follower_handler.find({"user_id": validated_data["user_id"]},
                                                        {"follower": 1, "_id": 1}).sort("_id", -1).limit(1))
        else:
            followers = list(self.follower_handler.find({"user_id": validated_data["user_id"],
                                                         "_id": {"$lt": ObjectId(validated_data["_id"])}},
                                                        {"follower": 1, "_id": 0}).sort("_id", -1).limit(1))
        for item in followers:
            item_id_convertor_to_string(item)
        return {"message": followers}


# ----------------done----------------
class FollowingsSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True, max_length=24, min_length=24)
    followings_handler = get_collection_handle(db_handler, "followings")

    def get(self, validated_data, page):
        if page == 1:
            followings = list(self.followings_handler.find({"user_id": validated_data["user_id"]},
                                                           {"following": 1, "_id": 1}).sort("_id", -1).limit(1))
        else:
            followings = list(self.followings_handler.find({"user_id": validated_data["user_id"],
                                                            "_id": {"$lt": ObjectId(validated_data["_id"])}},
                                                           {"following": 1, "_id": 0}).sort("_id", -1).limit(1))
        for item in followings:
            item_id_convertor_to_string(item)
        return {"message": followings}


class DeletePostSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True, max_length=24, min_length=24)
    post_id = serializers.CharField(required=True, max_length=24, min_length=24)
    post_handler = get_collection_handle(db_handler, "post")

    def get(self, validated_data):
        response = self.post_handler.remove(
            {"_id": ObjectId(validated_data["post_id"]), "user.id": validated_data["user_id"]})
        if response["ok"] == 1.0 and response["n"] == 1:
            CeleryTasksRobino.delete_post_for_followers.delay(validated_data["user_id"], validated_data["post_id"])
            CeleryTasksRobino.delete_post_comment.delay(validated_data["post_id"])
            return post_deleted
        return post_delete_forbidden


class DeleteCommentSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True, max_length=24, min_length=24)
    comment_id = serializers.CharField(required=True, max_length=24, min_length=24)
    comment_handler = get_collection_handle(db_handler, "comment")

    def get(self, validated_data):
        response = self.comment_handler.remove({"_id": ObjectId(validated_data["comment_id"]),
                                                "writer.id": validated_data["user_id"]})
        if response["ok"] == 1.0 and response["n"] == 1:
            CeleryTasksRobino.delete_comment_reply.delay(validated_data["comment_id"])
            return comment_deleted
        return comment_delete_forbidden
