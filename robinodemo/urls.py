from django.urls import path
from . import views


urlpatterns = [
    # list response
    path('robino/profile/home/<int:page>/', views.GetHome.as_view()),
    # single response
    path('robino/profile/add-comment/<str:post_id>/', views.AddComment.as_view()),
    path('robino/profile/reply-comment/<str:post_id>/<str:source_id>/', views.ReplyComment.as_view()),
    path('robino/profile/like-post/<str:post_id>/', views.LikeAPost.as_view()),
    # delete
    path('robino/profile/<str:post_id>/delete-post/', views.DeletePost.as_view()),
    path('robino/profile/<str:comment_id>/delete-comment/', views.DeleteComment.as_view()),
    # list response
    path('robino/profile/show-likes/<str:post_id>/<int:page>/', views.PostLikingUsers.as_view()),
    path('robino/profile/show-comments/<str:post_id>/<int:page>/', views.ShowComment.as_view()),
    path('robino/profile/show-replies/<str:comment_id>/<int:page>/', views.ShowReply.as_view()),
    path('robino/profile/show-followers/<int:page>/', views.Followers.as_view()),
    path('robino/profile/show-followings/<int:page>/', views.Followings.as_view()),
]


