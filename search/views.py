from django.utils.decorators import method_decorator
from ratelimit.decorators import ratelimit

from authenticate.permissions import AuthenticatedOnly
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import AccountQuerySerializer, PostQuerySerializer
from common.payloads import PayloadGenerator
from common.messages import *


class SearchAccount(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = AccountQuerySerializer

    # @method_decorator(ratelimit(key='header:x-real-ip', rate='2/m', method='POST', block=True))
    def post(self, request, page):
        payload = PayloadGenerator.search_account_payload(request.data["query"], request.data["_id"])
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().get(payload, page)
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)


class SearchPost(APIView):
    permission_classes = [AuthenticatedOnly]
    serializer_class = PostQuerySerializer

    @method_decorator(ratelimit(key='header:x-real-ip', rate='2/m', method='POST', block=True))
    # @ratelimit(field='username', rate='1/m')
    # @ratelimit(key='username', method='POST', rate='1/m')
    def post(self, request, page):
        payload = PayloadGenerator.search_post_payload(request.data["query"])
        if self.serializer_class(data=payload).is_valid(raise_exception=True):
            response = self.serializer_class().get(payload, page)
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data=wrong_input, status=status.HTTP_400_BAD_REQUEST)
