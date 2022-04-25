from django.urls import path
from .views import SearchPost, SearchAccount

urlpatterns = [
    path('post/<int:page>/', SearchPost.as_view()),
    path('profile/<int:page>/', SearchAccount.as_view()),
]
