from authenticate.permissions import AuthenticatedOnly
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializer import CommentSerializer, LikeSerializer, \
    PostLikingUsersSerializer, ShowCommentSerializer, FollowersSerializer, ShowRepliesSerializer, \
    FollowingsSerializer, ReplySerializer, DeletePostSerializer, DeleteCommentSerializer, UserHomeSerializer, \
    ProfileSerializer
from common.messages import *
from common.payloads import PayloadGenerator


class GetHome(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = UserHomeSerializer

    def post(self, request, page):
        payload = PayloadGenerator.home_payload(request.user["_id"])
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().get(payload, page)
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)


class GetProfileApiView(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = ProfileSerializer

    def get(self, request, page, username):
        payload = {"user_id": request.user["_id"], "username": username}
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().get(payload, page)
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)


class AddComment(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = CommentSerializer

    def post(self, request, post_id):
        payload = PayloadGenerator.add_comment_payload(request.data["content"], request.user["_id"], post_id)
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().create(payload)
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)


class ReplyComment(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = ReplySerializer

    def post(self, request, post_id, source_id):
        payload = PayloadGenerator.reply_comment_payload(request.data["content"], request.user["_id"], post_id,
                                                         source_id)
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().create(payload)
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)


class LikeAPost(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = LikeSerializer

    def post(self, request, post_id):
        payload = PayloadGenerator.like_post_payload(request.user["_id"], post_id)
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().create(payload)
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)


class PostLikingUsers(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = PostLikingUsersSerializer

    def post(self, request, post_id, page):
        payload = PayloadGenerator.post_liker_list_payload(post_id, request.data["_id"])
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().get(payload, page)
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)


class ShowComment(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = ShowCommentSerializer

    def get(self, request, post_id, page):
        payload = PayloadGenerator.show_comment_payload(request.user["_id"], post_id)
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().get(payload, page)
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)


class ShowReply(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = ShowRepliesSerializer

    def get(self, request, comment_id, page):
        payload = PayloadGenerator.show_reply_payload(request.data["_id"], comment_id)
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().get(payload, page)
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)


class Followers(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = FollowersSerializer

    def post(self, request, page):
        payload = PayloadGenerator.show_follower_payload(request.user["_id"])
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().get(payload, page)
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)


class Followings(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = FollowingsSerializer

    def post(self, request, page):
        payload = PayloadGenerator.show_following_payload(request.user["_id"], request.data["_id"])
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().get(payload, page)
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)


class DeletePost(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = DeletePostSerializer

    def post(self, request, post_id):
        payload = PayloadGenerator.delete_post_payload(request.user["_id"], post_id)
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().get(payload)
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)


class DeleteComment(GenericAPIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = DeleteCommentSerializer

    def post(self, request, comment_id):
        payload = PayloadGenerator.delete_comment_payload(request.user["_id"], comment_id)
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().get(payload)
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)
