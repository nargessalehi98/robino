# authenticate/urls.py
from authenticate import views
from django.urls import path

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout")
]
