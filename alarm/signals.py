from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Alarm
from .serializers import AlarmSerializer


@receiver(post_save, sender=Alarm)
def send_alarm(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        user = instance.user
        async_to_sync(channel_layer.group_send)(
            f"user{user.id}",
            {"type": "send_alarm", "message": AlarmSerializer(instance).data},
        )
