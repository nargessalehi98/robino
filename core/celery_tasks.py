from bson import ObjectId
from config.celery import app
from core.serializer import db_handler
from common.utils import get_collection_handle


class CeleryTasksRobino:
    @staticmethod
    @app.task
    def delete_post_for_followers(user_id, post_id):
        user_profile_handler = get_collection_handle(db_handler, 'userprofile')
        follower_handler = get_collection_handle(db_handler, 'followers')
        followers = list(follower_handler.find({"user_id": user_id}, {"user_id": 0, "_id": 0}))
        for item in followers:
            user_profile_handler.update_many({"_id": ObjectId(item["follower"])},
                                             {"$pull": {"new_posts": {"_id": ObjectId(post_id)}}})
        return True

    @staticmethod
    @app.task
    def update_followers_posts(user_id, post):
        followers_handler = get_collection_handle(db_handler, 'followers')
        user_profile_handler = get_collection_handle(db_handler, 'userprofile')
        follower_list = list(followers_handler.find({"user_id": user_id}, {"follower": 1, "_id": 0}))
        final_list = []
        for item in follower_list:
            final_list.append(ObjectId(item['follower']))
        # user_profile_handler.update_many({"_id": {"$in": final_list},{"$pop": {"new_posts": 1}})
        post['_id'] = ObjectId(post['_id'])
        user_profile_handler.update_many({"_id": {"$in": final_list}},
                                         {"$push": {"new_posts": {"$each": [post], "$sort": {"_id": -1}}}})
        return True

    @staticmethod
    @app.task
    def update_following_posts(user_id, profile_id):
        user_profile_handler = get_collection_handle(db_handler, 'userprofile')
        post_handler = get_collection_handle(db_handler, 'post')
        post_list = list(post_handler.find({"user.id": profile_id}).sort("_id", -1).limit(100))
        user_profile_handler.update_many({"_id": ObjectId(user_id)},
                                         {"$push": {"new_posts": {"$each": post_list, "$sort": {"_id": -1}}}})

        return True

    @staticmethod
    @app.task
    def delete_following_posts(user_id, profile_id):
        user_profile_handler = get_collection_handle(db_handler, 'userprofile')
        user_profile_handler.update_many({"_id": ObjectId(user_id)},
                                         {"$pull": {"new_posts": {"user.id": profile_id}}})
        return True

    @staticmethod
    @app.task
    def delete_post_comment(post_id):
        comment_handler = get_collection_handle(db_handler, 'comment')
        comment_handler.remove({"post_id": post_id})
        return True

    @staticmethod
    @app.task
    def delete_comment_reply(comment_id):
        comment_handler = get_collection_handle(db_handler, 'comment')
        comment_handler.remove({"source_id": comment_id})
        return True
