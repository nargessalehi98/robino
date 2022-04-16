import datetime
from pythonproject.celery import app
from bson import ObjectId
from rest_framework import serializers
from .utils import get_db_handle, get_collection_handle, item_id_convertor_to_string

db_handler, mongo_client = get_db_handle('robinodemo', 'localhost', '27017')
from .messages import *


# ----------------done----------------
class UserProfileSerializer(serializers.Serializer):
    user_id = serializers.CharField(read_only=True)

    def get(self, validated_data, page):
        post_handler = get_collection_handle(db_handler, 'post')
        if page == 1:
            post_list = list(post_handler.find({"user.id": str(validated_data["user_id"])},
                                               {"content": 1, "user": 1}).sort("_id", -1).limit(1))
        else:
            post_list = list(post_handler.find({"user.id": str(validated_data["user_id"]),
                                                "_id": {"$lt": ObjectId(validated_data['_id'])}},
                                               {"content": 1, "user": 1}).sort("_id", -1).limit(1))
        for item in post_list:
            item_id_convertor_to_string(item)
        return {"message": post_list}


# ----------------done----------------
class UserHomeSerializer(serializers.Serializer):

    def get(self, validated_data, page):
        user_profile_handler = get_collection_handle(db_handler, "user_profile")
        posts = list(user_profile_handler.find({"_id": ObjectId(validated_data["user_id"])},
                                               {"new_posts": {"$slice": [page - 1, 1]}, "_id": 0, "password": 0,
                                                "email": 0, "username": 0}))[0]['new_posts']
        for item in posts:
            item_id_convertor_to_string(item)
        return {"message": posts}


# ----------------change----------------
@app.task
def update_followers_posts(user_id, post):
    followers_handler = get_collection_handle(db_handler, 'followers')
    user_profile_handler = get_collection_handle(db_handler, 'user_profile')
    follower_list = list(followers_handler.find({"user_id": user_id}, {"follower": 1, "_id": 0}))
    final_list = []
    for item in follower_list:
        final_list.append(ObjectId(item['follower']))
    # user_profile_handler.update_many({"_id": {"$in": final_list},{"$pop": {"new_posts": 1}})
    post['_id'] = ObjectId(post['_id'])
    user_profile_handler.update_many({"_id": {"$in": final_list}},
                                     {"$push": {"new_posts": {"$each": [post], "$sort": {"_id": -1}}}})
    return True


# ----------------done----------------
class PostSerializer(serializers.Serializer):
    content = serializers.CharField(allow_null=False)
    user = serializers.CharField(allow_null=False)

    def create(self, validated_data):
        user_handler = get_collection_handle(db_handler, 'user_profile')
        post_handler = get_collection_handle(db_handler, 'post')

        user_id = validated_data["user"]
        validated_data["user"] = user_handler.find_one({"_id": ObjectId(validated_data["user"])},
                                                       {"_id": 0, "username": 1, "email": 1})
        validated_data["user"]["id"] = user_id
        post_handler.insert_one(validated_data)
        validated_data['_id'] = str(validated_data['_id'])
        validated_data['user'] = validated_data['user']['id']
        update_followers_posts.delay(user_id, validated_data)

        return {"message": post_added}


# ----------------done----------------
class CommentSerializer(serializers.Serializer):
    content = serializers.CharField(allow_null=False)
    post_id = serializers.IntegerField(allow_null=False)
    writer_id = serializers.IntegerField(allow_null=False)

    def create(self, validated_data):
        # user handler
        user_handler = get_collection_handle(db_handler, 'user_profile')
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
    content = serializers.CharField(allow_null=False)
    post_id = serializers.IntegerField(allow_null=False)
    writer_id = serializers.IntegerField(allow_null=False)

    def create(self, validated_data):
        # user handler
        user_handler = get_collection_handle(db_handler, 'user_profile')
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
    post_id = serializers.CharField(allow_null=False)
    liker_id = serializers.IntegerField(allow_null=False)

    def create(self, validated_data):
        like_handler = get_collection_handle(db_handler, 'like')
        user_handler = get_collection_handle(db_handler, 'user_profile')
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
    post_id = serializers.CharField(allow_null=False)

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
    post_id = serializers.CharField(allow_null=False)

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
    post_id = serializers.CharField(allow_null=False)

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
@app.task
def update_following_posts(user_id, profile_id):
    user_profile_handler = get_collection_handle(db_handler, 'user_profile')
    post_handler = get_collection_handle(db_handler, 'post')
    post_list = list(post_handler.find({"user.id": profile_id}).sort("_id", -1).limit(100))
    user_profile_handler.update_many({"_id": ObjectId(user_id)},
                                     {"$push": {"new_posts": {"$each": post_list, "$sort": {"_id": -1}}}})

    return True


# ----------------done----------------
@app.task
def delete_following_posts(user_id, profile_id):
    user_profile_handler = get_collection_handle(db_handler, 'user_profile')
    user_profile_handler.update_many({"_id": ObjectId(user_id)},
                                     {"$pull": {"new_posts": {"user.id": profile_id}}})
    return True


# ----------------done----------------
class FollowUnFollowSerializer(serializers.Serializer):
    user_id = serializers.CharField(allow_null=False)
    followings_handler = get_collection_handle(db_handler, "followings")
    followers_handler = get_collection_handle(db_handler, "followers")

    def create(self, validated_data):
        profile_id = validated_data["profile_id"]
        user_id = validated_data["user_id"]
        if self.followings_handler.find_one_and_delete({"user_id": user_id, "following": profile_id}):
            self.followers_handler.delete_one({"user_id": profile_id, "follower": user_id})
            delete_following_posts.delay(user_id, profile_id)
            return {"message": user_unfollowed}
        else:
            self.followings_handler.insert_one({"user_id": user_id, "following": profile_id})
            self.followers_handler.insert_one({"user_id": profile_id, "follower": user_id})
            update_following_posts.delay(user_id, profile_id)
        return {"message": user_followed}


# ----------------done----------------
class FollowersSerializer(serializers.Serializer):
    user_id = serializers.CharField(allow_null=False)
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
    user_id = serializers.CharField(allow_null=False)
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
