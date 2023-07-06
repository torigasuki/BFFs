from django.urls import path

from .views import AlarmView


urlpatterns = [
    path("", AlarmView.as_view(), name="alarm_view"),
    path("<int:alarm_id>/", AlarmView.as_view(), name="alarm_view"),
]
