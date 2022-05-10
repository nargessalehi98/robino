from django.utils.decorators import method_decorator
# from ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from common.messages import wrong_input
from .serializers import NotificationSerializer, DeleteNotificationSerializer
from authenticate.permissions import AuthenticatedOnly


class GetProfileNotification(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = NotificationSerializer

    # @method_decorator(ratelimit(key='header:x-real-ip', rate='2/m', method='GET', block=True))
    def get(self, request):
        payload = {"_id": str(request.user["_id"])}
        print(payload)
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().get(payload)
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)


class DeleteProfileNotification(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = DeleteNotificationSerializer

    # @method_decorator(ratelimit(key='header:x-real-ip', rate='2/m', method='GET', block=True))
    def get(self, request, notif_id):
        payload = {"_id": str(request.user["_id"]), "notif_id": notif_id}
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().get(payload)
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)
