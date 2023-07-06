from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from datetime import datetime
from pytz import timezone
from django.utils.timesince import timesince

from .models import Alarm
from community.models import Community
from feed.models import Category


class AlarmSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    community_name = serializers.SerializerMethodField()

    class Meta:
        model = Alarm
        fields = "__all__"

    def get_created_at(self, obj):
        now = datetime.now(timezone("Asia/Seoul"))
        return timesince(obj.created_at, now) + " 전"

    def get_community_name(self, obj):
        category = get_object_or_404(Category, id=obj.feed.category_id)
        communityurl = get_object_or_404(
            Community, title=category.community
        ).communityurl
        return communityurl
