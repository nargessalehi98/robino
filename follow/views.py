from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authenticate.permissions import AuthenticatedOnly
from common.messages import wrong_input
from common.payloads import PayloadGenerator
from .serializer import FollowUnFollowSerializer, GetRequestSerializer, AcceptRequestSerializer


class FollowUnFollow(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = FollowUnFollowSerializer

    def post(self, request, profile_id):
        payload = PayloadGenerator.follow_unfollow_payload(request.user["_id"], profile_id)
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            if request.data["profile_status"] == "True":
                response = self.serializer_class().create(payload)
            else:
                response = self.serializer_class().add(payload)
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)


class GetRequest(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = GetRequestSerializer

    def get(self, request):
        payload = {"user_id": str(request.user["_id"])}
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().get(payload)
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)


class AcceptRequest(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = AcceptRequestSerializer

    def post(self, request, request_id):
        payload = {"user_id": str(request.user["_id"]), "request_id": request_id}
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().get(payload)
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)
