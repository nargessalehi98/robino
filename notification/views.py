from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from common.messages import wrong_input
from .serializers import NotificationSerializer
from authenticate.permissions import AuthenticatedOnly


class GetProfileNotification(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = NotificationSerializer

    def get(self, request):
        payload = {"_id": request.user["_id"]}
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().get(payload)
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)
