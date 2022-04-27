from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authenticate.permissions import AuthenticatedOnly
from common.messages import wrong_input
from .serializer import UserProfileSerializer, FollowersSerializer, PostSerializer
from common.payloads import PayloadGenerator


class GetProfileApi(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = UserProfileSerializer

    def post(self, request, page):
        payload = PayloadGenerator.profile_payload(request.user["_id"], request.data["_id"])
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().get(payload, page)
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)


class GetFollowersApi(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = FollowersSerializer

    def post(self, request, page):
        payload = PayloadGenerator.followers_followings_payload(request.user["_id"], request.data["_id"])
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().get_follower(payload, page)
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)


class GetFollowingsApi(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = FollowersSerializer

    def post(self, request, page):
        payload = PayloadGenerator.followers_followings_payload(request.user["_id"], request.data["_id"])
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().get_following(payload, page)
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)


class AddPostApi(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = PostSerializer

    def post(self, request):
        payload = PayloadGenerator.add_post_payload(request.data["content"], request.user["_id"])
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().create(payload)
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)

