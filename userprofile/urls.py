from django.urls import path
from .views import GetProfileApi, GetFollowersApi, GetFollowingsApi, AddPostApi, ProfileSettingApi, \
    ProfileStatusApi, ChangeUsernameApi, ChangeEmailApi,ChangePasswordApi

urlpatterns = [
    path('robino/profile/<int:page>/', GetProfileApi.as_view()),
    path('robino/profile/followers/<int:page>/', GetFollowersApi.as_view()),
    path('robino/profile/followings/<int:page>/', GetFollowingsApi.as_view()),
    path('robino/profile/add-post/', AddPostApi.as_view()),
    path('robino/profile/setting/', ProfileSettingApi.as_view()),
    path('robino/profile/setting/username/', ChangeUsernameApi.as_view()),
    path('robino/profile/setting/password/', ChangePasswordApi.as_view()),
    path('robino/profile/setting/email/', ChangeEmailApi.as_view()),
    path('robino/profile/setting/status/', ProfileStatusApi.as_view()),
]
