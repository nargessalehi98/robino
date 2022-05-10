from bson import ObjectId
from rest_framework import serializers
from common.utils import get_collection_handle, get_db_handle, item_id_convertor_to_string

db_handler, mongo_client = get_db_handle('robinodemo', 'localhost', '27017')


class NotificationSerializer(serializers.Serializer):
    _id = serializers.CharField(required=True, max_length=24, min_length=24)
    notification_handler = get_collection_handle(db_handler, "notifications")

    def get(self, validated_data):
        notifications = list(self.notification_handler.find({"user_id": validated_data["_id"]}))
        for notification in notifications:
            item_id_convertor_to_string(notification)
        return {"message": notifications}


class DeleteNotificationSerializer(serializers.Serializer):
    _id = serializers.CharField(required=True, max_length=24, min_length=24)
    notif_id = serializers.CharField(required=True, max_length=24, min_length=24)
    notification_handler = get_collection_handle(db_handler, "notifications")

    def get(self, validated_data):
        result = self.notification_handler.remove(
            {"_id": ObjectId(validated_data["notif_id"]), "user_id": validated_data["_id"]})
        return {"message": result}
