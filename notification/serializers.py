from rest_framework import serializers
from common.utils import get_collection_handle, get_db_handle, item_id_convertor_to_string

db_handler, mongo_client = get_db_handle('robinodemo', 'localhost', '27017')


class NotificationSerializer(serializers.Serializer):
    _id = serializers.CharField(required=True, max_length=24, min_length=24)
    notification_handler = get_collection_handle(db_handler, "notification")

    def get(self, validated_data):
        notifications = list(self.notification_handler({"user_id": validated_data["_id"]}))
        for notification in notifications:
            item_id_convertor_to_string(notification)
        return {"message": notifications}
