from datetime import datetime
from pytz import timezone
from rest_framework import serializers
from decouple import config

from community.models import Community
from feed.models import (
    Category,
    Comment,
    Cocomment,
    Feed,
    GroupPurchase,
    JoinedUser,
    GroupPurchaseComment,
)
from user.models import Profile
from django.db.models import Sum


class CategorySerializer(serializers.ModelSerializer):
    """카테고리 serializer"""

    class Meta:
        model = Category
        fields = [
            "category_name",
        ]


class CocommentSerializer(serializers.ModelSerializer):
    """대댓글 serializer"""

    user_id = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = Cocomment
        fields = [
            "id",
            "user",
            "user_id",
            "nickname",
            "text",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "user": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def get_nickname(self, obj):
        return Profile.objects.get(user=obj.user).nickname

    def get_user_id(self, obj):
        return Profile.objects.get(user=obj.user).id


class CommentCreateSerializer(serializers.ModelSerializer):
    """댓글 생성 serializer"""

    class Meta:
        model = Comment
        fields = [
            "text",
        ]

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment


class CommentSerializer(serializers.ModelSerializer):
    """댓글 serializer"""

    user_id = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    cocomment = CocommentSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "user_id",
            "nickname",
            "text",
            "created_at",
            "updated_at",
            "cocomment",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "user": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def get_user_id(self, obj):
        return Profile.objects.get(user=obj.user).id

    def get_nickname(self, obj):
        return Profile.objects.get(user=obj.user).nickname

    def get_cocomment(self, obj):
        return obj.cocomment.all()


class FeedTitleSerializer(serializers.ModelSerializer):
    """feed 제목 serializer"""

    class Meta:
        model = Feed
        fields = [
            "id",
            "category",
            "title",
            "view_count",
        ]


class FeedListSerializer(serializers.ModelSerializer):
    """feed 리스트 serializer"""

    nickname = serializers.SerializerMethodField()
    profileimage = serializers.SerializerMethodField()
    profileimageurl = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    community_name = serializers.SerializerMethodField()

    class Meta:
        model = Feed
        fields = [
            "id",
            "user",
            "nickname",
            "profileimage",
            "profileimageurl",
            "title",
            "content",
            "view_count",
            "created_at",
            "category",
            "comments_count",
            "likes_count",
            "is_notification",
            "community_name",
        ]

    def get_nickname(self, obj):
        return Profile.objects.get(user=obj.user).nickname

    def get_profileimage(self, obj):
        return str(Profile.objects.get(user=obj.user).profileimage)

    def get_profileimageurl(self, obj):
        return (
            config("BACKEND_URL")
            + "/media/"
            + str(Profile.objects.get(user=obj.user).profileimage)
        )

    def get_category(self, obj):
        return Category.objects.get(id=obj.category_id).category_name

    def get_comments_count(self, obj):
        comment = obj.comment.count()
        cocomment = Cocomment.objects.filter(comment__feed=obj).count()
        return comment + cocomment

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_community_name(self, obj):
        category = Category.objects.get(id=obj.category_id)
        communityurl = Community.objects.get(title=category.community).communityurl
        return communityurl


class FeedCreateSerializer(serializers.ModelSerializer):
    """feed 생성 serializer"""

    class Meta:
        model = Feed
        fields = [
            "title",
            "content",
            "category",
        ]
        extra_kwargs = {
            "category": {"read_only": True},
        }


class FeedDetailSerializer(serializers.ModelSerializer):
    """feed 상세 serializer"""

    likes_count = serializers.SerializerMethodField()
    likes = serializers.StringRelatedField(many=True)
    nickname = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    category_url = serializers.SerializerMethodField()
    like_bool = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Feed
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "user": {"read_only": True},
            "nickname": {"read_only": True},
            "category_name": {"read_only": True},
            "category_url": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "likes": {"read_only": True},
            "like_bool": {"read_only": True},
        }

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_nickname(self, obj):
        return Profile.objects.get(user=obj.user).nickname

    def get_category_name(self, obj):
        return Category.objects.get(id=obj.category_id).category_name

    def get_category_url(self, obj):
        return Category.objects.get(id=obj.category_id).category_url

    def get_like_bool(self, obj):
        request = self.context.get("request")
        if request.user in obj.likes.all():
            return True
        else:
            return False

    def get_comments_count(self, obj):
        comment = obj.comment.count()
        cocomment = Cocomment.objects.filter(comment__feed=obj).count()
        return comment + cocomment


class ProfileFeedSerializer(serializers.ModelSerializer):
    """feed 상세 serializer"""

    nickname = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Feed
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "user": {"read_only": True},
            "nickname": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_nickname(self, obj):
        return Profile.objects.get(user=obj.user).nickname

    def get_comments_count(self, obj):
        comment = obj.comment.count()
        cocomment = Cocomment.objects.filter(comment__feed=obj).count()
        return comment + cocomment


class FeedNotificationSerializer(serializers.ModelSerializer):
    """feed 공지 serializer"""

    class Meta:
        model = Feed
        fields = [
            "is_notification",
        ]

    def post_is_notification(self, obj, community, request):
        """공지 field 상태 check"""
        if not obj.is_notification:
            return False
        elif obj.is_notification:
            return True


class GroupPurchaseListSerializer(serializers.ModelSerializer):
    """공구 게시글 list serializer"""

    grouppurchase_status = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    joined_user_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = GroupPurchase
        fields = [
            "id",
            "title",
            "product_name",
            "person_limit",
            "location",
            "user",
            "nickname",
            "open_at",
            "close_at",
            "is_ended",
            "created_at",
            "grouppurchase_status",
            "is_ended",
            "view_count",
            "comments_count",
            "joined_user_count",
        ]

    def get_nickname(self, obj):
        return Profile.objects.get(user=obj.user).nickname

    def get_joined_user_count(self, obj):
        real_join = JoinedUser.objects.filter(
            grouppurchase_id=obj.id, is_deleted=False
        ).count()
        return real_join

    def get_comments_count(self, obj):
        return obj.p_comment.count()

    def get_grouppurchase_status(self, obj):
        """공구 게시글 상태 check"""
        now = datetime.now(timezone("Asia/Seoul"))
        is_ended = obj.is_ended
        open_at = datetime.strptime(str(obj.open_at), "%Y-%m-%d %H:%M:%S%z")
        if not obj.close_at:
            if is_ended:
                return "종료"
            elif not is_ended and open_at > now:
                return "시작 전"
            elif not is_ended and open_at < now:
                return "진행 중"
        else:
            close_at = datetime.strptime(str(obj.open_at), "%Y-%m-%d %H:%M:%S%z")
            if is_ended:
                return "종료"
            elif close_at < now:
                # cron 작동 안했을 경우에도 종료 시간에따라 종료를 띄워주기
                return "종료"
            elif not is_ended and open_at > now:
                return "시작 전"
            elif close_at and not is_ended and close_at > now and open_at < now:
                return "진행 중"


class GroupPurchaseDetailSerializer(serializers.ModelSerializer):
    """공구 게시글 상세 serializer"""

    grouppurchase_status = serializers.SerializerMethodField()
    purchase_quantity = serializers.SerializerMethodField()
    joined_user_count = serializers.SerializerMethodField()
    joined_users = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    end_choice = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    category_url = serializers.SerializerMethodField()

    class Meta:
        model = GroupPurchase
        fields = "__all__"

    def get_grouppurchase_status(self, obj):
        """공구 게시글 상태 check"""
        now = datetime.now(timezone("Asia/Seoul"))
        is_ended = obj.is_ended
        open_at = datetime.strptime(str(obj.open_at), "%Y-%m-%d %H:%M:%S%z")
        if not obj.close_at:
            if is_ended:
                return "종료"
            elif not is_ended and open_at > now:
                return "시작 전"
            elif not is_ended and open_at < now:
                return "진행 중"
        else:
            close_at = datetime.strptime(str(obj.close_at), "%Y-%m-%d %H:%M:%S%z")
            if is_ended:
                return "종료"
            elif close_at < now:
                # cron 작동 안했을 경우에도 종료 시간에따라 종료를 띄워주기
                return "종료"
            elif not is_ended and open_at > now:
                return "시작 전"
            elif close_at and not is_ended and close_at > now and open_at < now:
                return "진행 중"

    def get_joined_users(self, obj):
        real_join = JoinedUser.objects.filter(grouppurchase_id=obj.id, is_deleted=False)
        serializer = JoinedUserListSerializer(real_join, many=True)
        return serializer.data

    def get_joined_user_count(self, obj):
        real_join = JoinedUser.objects.filter(
            grouppurchase_id=obj.id, is_deleted=False
        ).count()
        return real_join

    def get_purchase_quantity(self, obj):
        return (
            JoinedUser.objects.filter(grouppurchase_id=obj.id)
            .aggregate(Sum("product_quantity"))
            .get("product_quantity__sum")
            or 0
        )

    def get_comments_count(self, obj):
        return obj.p_comment.count()

    def get_end_choice(self, obj):
        return obj.get_end_option_display(obj)

    def get_category_name(self, obj):
        return obj.category.category_name

    def get_category_url(self, obj):
        return obj.category.category_url


class GroupPurchaseCreateSerializer(serializers.ModelSerializer):
    """공구 게시글 생성 serializer"""

    class Meta:
        model = GroupPurchase
        fields = [
            "title",
            "content",
            "product_name",
            "product_number",
            "product_price",
            "link",
            "person_limit",
            "location",
            "meeting_at",
            "open_at",
            "close_at",
            "end_option",
        ]
        extra_kwargs = {
            "user": {"read_only": True},
            "community": {"read_only": True},
            "category": {"read_only": True},
        }

    def validate_datetime(self, data):
        """공구 create 시 시간유효성 validate"""
        now = datetime.now()
        open_at = datetime.strptime(data.get("open_at"), "%Y-%m-%dT%H:%M:%S")
        meeting_at = datetime.strptime(data.get("meeting_at"), "%Y-%m-%dT%H:%M:%S")
        close = data.get("close_at")
        if not close:
            if now > open_at:
                raise serializers.ValidationError(
                    {"error": "모집 시작시간 오류. 현재 이후의 시점을 선택해주세요."}
                )
            if open_at >= meeting_at:
                raise serializers.ValidationError(
                    {"error": "만날시간 오류. 모집 시작보다 이후의 시점을 선택해주세요."}
                )
            return data
        close_at = datetime.strptime(close, "%Y-%m-%dT%H:%M:%S")
        if now > open_at:
            raise serializers.ValidationError(
                {"error": "모집 시작시간 오류. 현재 이후의 시점을 선택해주세요."}
            )
        if open_at >= close_at:
            raise serializers.ValidationError(
                {"error": "모집 종료시간 오류. 모집 시작보다 이후의 시점을 선택해주세요."}
            )
        if close_at > meeting_at:
            raise serializers.ValidationError(
                {"error": "만날시간 오류. 모집 종료보다 이후의 시점을 선택해주세요."}
            )
        return data

    def validate_datetime_update(self, data):
        """공구 update 시 시간유효성 validate"""
        now = datetime.now()
        open_at = datetime.strptime(data.get("open_at"), "%Y-%m-%dT%H:%M:%S")
        meeting_at = datetime.strptime(data.get("meeting_at"), "%Y-%m-%dT%H:%M:%S")
        close = data.get("close_at")
        if not close:
            if open_at >= meeting_at:
                raise serializers.ValidationError(
                    {"error": "만날시간 오류. 모집 시작보다 이후의 시점을 선택해주세요."}
                )
            if now > meeting_at:
                raise serializers.ValidationError(
                    {"error": "만날시간 오류. 현재 이후의 시점을 선택해주세요."}
                )
            return data
        close_at = datetime.strptime(close, "%Y-%m-%dT%H:%M:%S")
        if now > close_at or open_at > close_at:
            raise serializers.ValidationError(
                {"error": "모집 종료시간 오류. 현재 이후의 시점을 선택해주세요."}
            )
        if meeting_at < close_at:
            raise serializers.ValidationError(
                {"error": "만날시간 오류. 모집 종료보다 이후의 시점을 선택해주세요."}
            )
        return data


class GroupPurchaseSelfEndSerializer(serializers.ModelSerializer):
    """공구 종료 serializer"""

    class Meta:
        model = GroupPurchase
        fields = [
            "is_ended",
        ]


class JoinedUserCreateSerializer(serializers.ModelSerializer):
    """공구 참여유저 생성 serializer"""

    class Meta:
        model = JoinedUser
        fields = [
            "product_quantity",
        ]
        extra_kwargs = {
            "user": {"read_only": True},
            "grouppurchase": {"read_only": True},
            "created_at": {"read_only": True},
            "is_deleted": {"read_only": True},
        }


class JoinedUserSerializer(serializers.ModelSerializer):
    """공구 참여유저 serializer"""

    class Meta:
        model = JoinedUser
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True},
            "grouppurchase": {"read_only": True},
        }


class JoinedUserListSerializer(serializers.ModelSerializer):
    """공구 참여유저 serializer"""

    nickname = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()
    profileimage = serializers.SerializerMethodField()

    class Meta:
        model = JoinedUser
        fields = [
            "id",
            "user",
            "product_quantity",
            "created_at",
            "nickname",
            "region",
            "profileimage",
        ]

    def get_nickname(self, obj):
        return obj.user.profile.nickname

    def get_region(self, obj):
        return obj.user.profile.region

    def get_profileimage(self, obj):
        return f"{obj.user.profile.profileimage}"


class FeedSearchSerializer(serializers.ModelSerializer):
    """피드 검색 serializer"""

    class Meta:
        model = Feed
        fields = "__all__"


class GroupPurchaseCommentSerializer(serializers.ModelSerializer):
    """공구 댓글 serializer"""

    user_id = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = GroupPurchaseComment
        fields = [
            "id",
            "user_id",
            "nickname",
            "text",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "user": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def get_user_id(self, obj):
        return Profile.objects.get(user=obj.user).id

    def get_nickname(self, obj):
        return Profile.objects.get(user=obj.user).nickname


class ProfileGrouppurchaseSerializer(serializers.ModelSerializer):
    community_url = serializers.SerializerMethodField()

    class Meta:
        model = GroupPurchase
        fields = ["id", "title", "product_name", "open_at", "close_at", "community_url"]

    def get_community_url(self, obj):
        return obj.community.communityurl
