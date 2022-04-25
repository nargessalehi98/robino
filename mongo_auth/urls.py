# mongo_auth/urls.py
from mongo_auth import views
from django.urls import path

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout")
]
