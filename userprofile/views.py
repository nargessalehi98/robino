from django.utils.decorators import method_decorator
# from ratelimit.decorators import ratelimit
# from ratelimit.mixins import RatelimitMixin
from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from authenticate.permissions import AuthenticatedOnly
from common.messages import wrong_input
from .serializer import UserProfileSerializer, FollowersSerializer, PostSerializer, ProfileStatusSerializer, \
    SettingSerializer, ChangeUsernameSerializer, ChangeEmailSerializer, ChangePasswordSerializer
from common.payloads import PayloadGenerator
from common.utils import email_is_valid, password_is_valid
from authenticate.utils import pwd_context


class GetProfileApi(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = UserProfileSerializer

    # @method_decorator(ratelimit(key='header:x-real-ip', rate='2/m', method='POST', block=True))
    def post(self, request, page):
        payload = PayloadGenerator.profile_payload(request.user["_id"], request.data["_id"])
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().get(payload, page)
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)


class GetFollowersApi(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = FollowersSerializer

    # @method_decorator(ratelimit(key='header:x-real-ip', rate='2/m', method='POST', block=True))
    def post(self, request, page):
        payload = PayloadGenerator.followers_followings_payload(request.user["_id"], request.data["_id"])
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().get_follower(payload, page)
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)


class GetFollowingsApi(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = FollowersSerializer

    # @method_decorator(ratelimit(key='header:x-real-ip', rate='2/m', method='POST', block=True))
    def post(self, request, page):
        payload = PayloadGenerator.followers_followings_payload(request.user["_id"], request.data["_id"])
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().get_following(payload, page)
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)


class AddPostApi(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = PostSerializer

    # @method_decorator(ratelimit(key='header:x-real-ip', rate='2/m', method='POST', block=True))
    def post(self, request):
        payload = PayloadGenerator.add_post_payload(request.data["content"], request.user["_id"])
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().create(payload)
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)


class ProfileSettingApi(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = SettingSerializer

    # @method_decorator(ratelimit(key='header:x-real-ip', rate='2/m', method='POST', block=True))
    def get(self, request):
        payload = {"_id": str(request.user["_id"])}
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().get(payload)
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)


class ChangeUsernameApi(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = ChangeUsernameSerializer

    # @method_decorator(ratelimit(key='header:x-real-ip', rate='2/m', method='POST', block=True))
    def post(self, request):
        payload = {"_id": str(request.user["_id"]), "username": request.data["username"]}
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().get(payload)
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)


class ChangeEmailApi(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = ChangeEmailSerializer

    # @method_decorator(ratelimit(key='header:x-real-ip', rate='2/m', method='POST', block=True))
    def post(self, request):
        payload = {"_id": str(request.user["_id"]), "email": request.data["email"]}
        if self.serializer_class(data=payload).is_valid(raise_exception=True) and email_is_valid(request.data["email"]):
            response = self.serializer_class().get(payload)
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordApi(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = ChangePasswordSerializer

    # @method_decorator(ratelimit(key='header:x-real-ip', rate='2/m', method='POST', block=True))
    def post(self, request):
        payload = {"_id": str(request.user["_id"]), "password": pwd_context.hash(request.data["password"])}
        if self.serializer_class(data=payload).is_valid(raise_exception=True) and password_is_valid(
                request.data["password"]):
            response = self.serializer_class().get(payload)
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)


class ProfileStatusApi(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = ProfileStatusSerializer

    # @method_decorator(ratelimit(key='header:x-real-ip', rate='2/m', method='POST', block=True))
    def post(self, request):
        payload = {"_id": str(request.user["_id"])}
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().create(payload)
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)
