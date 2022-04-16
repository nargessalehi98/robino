import datetime
import time

from mongo_auth.permissions import AuthenticatedOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializer import UserProfileSerializer, CommentSerializer, \
    PostSerializer, LikeSerializer, \
    PostLikingUsersSerializer, UserHomeSerializer, ShowCommentSerializer, \
    FollowUnFollowSerializer, FollowersSerializer, ShowRepliesSerializer, FollowingsSerializer, ReplySerializer
from .messages import *


class GetProfile(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = UserProfileSerializer

    def post(self, request, page):
        payload = {
            "user_id": str(request.user['_id']),
            "_id": request.data["_id"],
        }
        if self.serializer_class(data=payload).is_valid():
            response = self.serializer_class().get(payload, page)
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)


class GetHome(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = UserHomeSerializer

    def post(self, request, row):
        payload = {
            "user_id": str(request.user['_id']),
        }
        if self.serializer_class(data=payload).is_valid():
            response = self.serializer_class().get(payload, row)
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)


class AddPost(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = PostSerializer

    def post(self, request):
        payload = {
            "content": request.data['content'],
            "user": str(request.user['_id']),
        }
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().create(payload)
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)


class AddComment(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = CommentSerializer

    def post(self, request, post_id):
        payload = {
            "content": request.data['content'],
            "writer": str(request.user['_id']),
            "post_id": post_id,
            "replies": 0
        }
        response = self.serializer_class().create(payload)
        return Response(data=response, status=status.HTTP_201_CREATED)


class ReplyComment(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = ReplySerializer

    def post(self, request, post_id, source_id):
        payload = {
            "content": request.data['content'],
            "writer": str(request.user['_id']),
            "post_id": post_id,
            "source_id": source_id
        }
        response = self.serializer_class().create(payload)
        return Response(data=response, status=status.HTTP_201_CREATED)


# ----------------done----------------
class LikeAPost(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = LikeSerializer

    def post(self, request, post_id):
        payload = {
            "liker": str(request.user['_id']),
            "post_id": post_id
        }
        response = self.serializer_class().create(payload)
        return Response(data=response, status=status.HTTP_201_CREATED)


class PostLikingUsers(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = PostLikingUsersSerializer

    def post(self, request, post_id, page):
        payload = {
            "post_id": post_id,
            "_id": request.data["_id"]
        }
        response = self.serializer_class().get(payload, page)
        return Response(data=response, status=status.HTTP_201_CREATED)


class ShowComment(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = ShowCommentSerializer

    def get(self, request, post_id, page):
        payload = {
            "_id": request.data["_id"],
            "post_id": post_id,
        }
        response = self.serializer_class().get(payload, page)
        return Response(data=response, status=status.HTTP_201_CREATED)


class ShowReply(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = ShowRepliesSerializer

    def get(self, request, comment_id, page):
        payload = {
            "_id": request.data["_id"],
            "comment_id": comment_id,
        }
        response = self.serializer_class().get(payload, page)
        return Response(data=response, status=status.HTTP_201_CREATED)


class FollowUnFollow(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = FollowUnFollowSerializer

    def post(self, request, profile_id):
        data = {
            "user_id": str(request.user['_id']),
            "profile_id": profile_id
        }
        response = self.serializer_class().create(data)
        return Response(data=response, status=status.HTTP_201_CREATED)


class Followers(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = FollowersSerializer

    def post(self, request, page):
        data = {
            "user_id": str(request.user['_id']),
        }
        response = self.serializer_class().get(data, page)
        return Response(data=response, status=status.HTTP_201_CREATED)


class Followings(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = FollowingsSerializer

    def post(self, request, page):
        data = {
            "user_id": str(request.user['_id']),
            "_id": request.data["_id"]
        }
        response = self.serializer_class().get(data, page)
        return Response(data=response, status=status.HTTP_201_CREATED)
