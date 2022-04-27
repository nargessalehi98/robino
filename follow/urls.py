from django.urls import path
from .views import FollowUnFollow, GetRequest, AcceptRequest

urlpatterns = [
    path('robino/profile/<str:profile_id>/funf/', FollowUnFollow.as_view()),
    path('robino/profile/requests/', GetRequest.as_view()),
    path('robino/profile/request/<str:request_id>/', AcceptRequest.as_view())
]
