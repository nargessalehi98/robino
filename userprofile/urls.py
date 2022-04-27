from django.urls import path
from .views import GetProfileApi, GetFollowersApi, GetFollowingsApi, AddPostApi

urlpatterns = [
    path('robino/profile/<int:page>/', GetProfileApi.as_view()),
    path('robino/profile/followers/<int:page>/', GetFollowersApi.as_view()),
    path('robino/profile/followings/<int:page>/', GetFollowingsApi.as_view()),
    path('robino/profile/add-post/', AddPostApi.as_view()),
]
