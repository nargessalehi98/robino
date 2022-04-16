from django.urls import path, include
from . import views

urlpatterns = [
    path('robinodemo/', include('mongo_auth.urls')),
    # list response
    path('robinodemo/profile/<int:page>/', views.GetProfile.as_view()),
    path('robinodemo/profile/home/<int:row>/', views.GetHome.as_view()),
    # single response
    path('robinodemo/profile/add-post/', views.AddPost.as_view()),
    path('robinodemo/profile/add-comment/<str:post_id>/', views.AddComment.as_view()),
    path('robinodemo/profile/reply-comment/<str:post_id>/<str:source_id>/', views.ReplyComment.as_view()),
    path('robinodemo/profile/like-post/<str:post_id>/', views.LikeAPost.as_view()),
    path('robinodemo/profile/<str:profile_id>/funf/', views.FollowUnFollow.as_view()),
    # list response
    path('robinodemo/profile/show-likes/<str:post_id>/<int:page>/', views.PostLikingUsers.as_view()),
    path('robinodemo/profile/show-comments/<str:post_id>/<int:page>/', views.ShowComment.as_view()),
    path('robinodemo/profile/show-replies/<str:comment_id>/<int:page>/', views.ShowReply.as_view()),
    path('robinodemo/profile/show-followers/<int:page>/', views.Followers.as_view()),
    path('robinodemo/profile/show-followings/<int:page>/', views.Followings.as_view()),
]
