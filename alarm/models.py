from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from user.models import User
from feed.models import Feed, Comment, Cocomment


class Alarm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=Comment)
def create_comment_alarm(sender, instance, created, **kwargs):
    if created:
        Alarm.objects.create(
            user=instance.feed.user,
            feed=instance.feed,
            message="피드에 새로운 댓글이 달렸습니다!",
        )


@receiver(post_save, sender=Cocomment)
def create_cocomment_alarm(sender, instance, created, **kwargs):
    if created:
        Alarm.objects.create(
            user=instance.comment.user,
            feed=instance.comment.feed,
            message="댓글에 새로운 댓글이 달렸습니다!",
        )
