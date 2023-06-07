from rest_framework import serializers
from feed.models import Feed, Comment, Cocomment, Category, GroupPurchase
from django.utils import timezone


class CategorySerializer:
    class Meta:
        model = Category
        fields = "__all__"


class CocommentSerializer:
    class Meta:
        model = Cocomment
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "user": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }


class CommentSerializer:
    cocomment = CocommentSerializer(required=False)

    class Meta:
        model = Comment
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "user": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "cocomment": {"read_only": True},
        }


class FeedListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = [
            "user",
            "title",
            "image",
            "view_count",
            "created_at",
        ]


class FeedCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = [
            "title",
            "content",
            "image",
            "video",
        ]


class FeedDetailSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Feed
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "user": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "likes": {"read_only": True},
        }

    def get_comments_count(self, obj):
        return obj.comment.count() + obj.cocomment.count()

    def get_likes_count(self, obj):
        return obj.likes.count()


class GroupPurchaseSerializer:
    class Meta:
        model = GroupPurchase
        fields = "__all__"

    def validate_datetime(self, data):
        now = timezone.now
        started_at = data.get("started_at")
        ended_at = data.get("ended_at")
        if now > started_at:
            raise serializers.ValidationError({"error": "현재 이후의 시점을 선택해주세요."})
        if ended_at and started_at > ended_at:
            raise serializers.ValidationError({"error": "시작 시간보다 이후의 시점을 선택해주세요."})
        return data
