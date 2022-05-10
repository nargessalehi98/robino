from django.urls import path
from .views import GetProfileNotification,DeleteProfileNotification

urlpatterns = [
    path('robino/profile/notification/', GetProfileNotification.as_view()),
    path('robino/profile/notification/<str:notif_id>/delete/', DeleteProfileNotification.as_view())
]
