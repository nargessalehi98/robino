from bson import ObjectId
from rest_framework import serializers
from robinodemo.utils import get_db_handle, get_collection_handle, item_id_convertor_to_string
from .inverted_index import search_query

db_handler, mongo_client = get_db_handle('robinodemo', 'localhost', '27017')


class AccountQuerySerializer(serializers.Serializer):
    query = serializers.RegexField(regex='^[a-zA-Z0-9_.-]*$', required=True)
    _id = serializers.CharField(allow_blank=True, max_length=24, min_length=24)
    profile_handler = get_collection_handle(db_handler, 'userprofile')

    def get(self, validated_data, page):
        regex = str(validated_data["query"])
        if page == 1:
            profiles = list(self.profile_handler.find({"username": {"$regex": regex, "$options": "i"}},
                                                      {"_id": 1, "username": 1}).sort("_id", -1).limit(1))
        else:
            profiles = list(self.profile_handler.find({"username": {"$regex": regex, "$options": "i"},
                                                       "_id": {"$lt": ObjectId(validated_data["_id"])}},
                                                      {"_id": 1, "username": 1}).sort("_id", -1).limit(1))
        for item in profiles:
            item_id_convertor_to_string(item)
        return {"message": profiles}


class PostQuerySerializer(serializers.Serializer):
    query = serializers.CharField(required=True, max_length=240)
    post_handler = get_collection_handle(db_handler, 'post')

    def get(self, validated_data, page):
        response = search_query(validated_data["query"])
        posts = list(self.post_handler.find({"_id": {"$in": response}}).skip(page - 1).limit(1))
        for item in posts:
            item_id_convertor_to_string(item)
        return {"message": posts}
