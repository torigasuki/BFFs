import json
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Alarm
from .serializers import AlarmSerializer
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Alarm)
def send_alarm(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        user_id = instance.user.id
        async_to_sync(channel_layer.group_send)(
            f"user{user_id}",
            {"type": "send_alarm", "message": AlarmSerializer(instance).data},
        )


def get_alarm(user):
    notifications = Alarm.objects.filter(user=user)
    serializer = AlarmSerializer(notifications, many=True)
    return serializer.data


class AlarmConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        self.group_name = f"user{user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        alarms = await database_sync_to_async(get_alarm)(user)

        if alarms:
            await self.channel_layer.group_send(
                self.group_name, {"type": "send_alarm", "message": alarms}
            )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_alarm(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({"message": message}))
