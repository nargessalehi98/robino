from django.urls import path
from .views import GetProfileNotification

urlpatterns = [
    path('robino/profile/notification/', GetProfileNotification.as_view()),
    path('robino/profile/notification/<str:notif_id>/delete/', GetProfileNotification.as_view())
]
