from rest_framework import serializers
from decouple import config

from user.models import User
from feed.models import Feed
from feed.serializers import FeedTitleSerializer
from .models import Community, CommunityAdmin, ForbiddenWord
from .validators import can_only_eng_and_int


class CommunitySerializer(serializers.ModelSerializer):
    imageurl = serializers.SerializerMethodField()
    bookmarked = serializers.SerializerMethodField()
    forbiddenword = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    feeds = serializers.SerializerMethodField()
    admin = serializers.SerializerMethodField()

    class Meta:
        model = Community
        fields = [
            "id",
            "title",
            "communityurl",
            "introduction",
            "image",
            "imageurl",
            "is_approval",
            "bookmarked",
            "forbiddenword",
            "categories",
            "feeds",
            "admin",
        ]

    def get_imageurl(self, obj):
        return config("BACKEND_URL") + "/media/" + str(obj.image)

    def get_bookmarked(self, obj):
        return obj.bookmarked.count()

    def get_forbiddenword(self, obj):
        words = obj.forbiddenword.all()
        return [forbidden.word for forbidden in words]

    def get_categories(self, obj):
        categories = obj.community_category.all()
        category_name_list = [
            [category.id, category.category_name, category.category_url]
            for category in categories
        ]
        return category_name_list

    def get_feeds(self, obj):
        feeds = Feed.objects.filter(category__community=obj)
        feed = FeedTitleSerializer(feeds, many=True)
        return feed.data

    def get_admin(self, obj):
        admin = CommunityAdmin.objects.filter(community=obj)
        admin_serializer = CommunityAdminSerializer(admin, many=True)
        return admin_serializer.data


class CommunityCategorySerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Community
        fields = [
            "categories",
        ]

    def get_categories(self, obj):
        categories = obj.community_category.all()
        category_name_list = [
            [category.id, category.category_name] for category in categories
        ]
        return category_name_list


class CommunityCreateSerializer(serializers.ModelSerializer):
    imageurl = serializers.SerializerMethodField()

    class Meta:
        model = Community
        fields = [
            "id",
            "title",
            "communityurl",
            "introduction",
            "image",
            "imageurl",
            "is_approval",
        ]

    def create(self, validated_data):
        title = validated_data.get("title")
        communityurl = validated_data.get("communityurl")
        if Community.objects.filter(title=title).exists():
            raise serializers.ValidationError("이미 존재하는 커뮤니티 이름입니다.")
        if not can_only_eng_and_int(communityurl):
            raise serializers.ValidationError("커뮤니티url은 영어와 숫자로 5글자 이상인 경우에 작성가능합니다.")

        introduction = validated_data.get("introduction")
        image = validated_data.get("image")

        community = Community.objects.create(
            title=title,
            communityurl=communityurl,
            introduction=introduction,
            image=image,
        )
        return community

    def get_imageurl(self, obj):
        return config("BACKEND_URL") + "/media/" + str(obj.image)


class CommunityUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = [
            "introduction",
            "image",
        ]


class CommunityAdminCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityAdmin
        fields = [
            "user",
        ]


class MyCommunitySerializer(serializers.ModelSerializer):
    title = serializers.StringRelatedField(source="community.title")
    communityurl = serializers.StringRelatedField(source="community.communityurl")
    introduction = serializers.StringRelatedField(source="community.introduction")
    image = serializers.StringRelatedField(source="community.image")
    imageurl = serializers.SerializerMethodField()

    class Meta:
        model = CommunityAdmin
        fields = [
            "user",
            "title",
            "communityurl",
            "introduction",
            "image",
            "imageurl",
        ]

    def get_imageurl(self, obj):
        return config("BACKEND_URL") + "/media/" + str(obj.community.image)


class CommunityAdminSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(source="user.email")
    name = serializers.StringRelatedField(source="user.name")
    nickname = serializers.StringRelatedField(source="user.profile.nickname")
    last_login = serializers.StringRelatedField(source="user.last_login")

    class Meta:
        model = CommunityAdmin
        fields = [
            "user_id",
            "user",
            "name",
            "nickname",
            "is_comuadmin",
            "is_subadmin",
            "last_login",
        ]


class CommunityUrlSerializer(serializers.ModelSerializer):
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = Community
        fields = ["title", "communityurl", "is_bookmarked"]

    def get_is_bookmarked(self, obj):
        request = self.context.get("request")
        if request.user.is_authenticated:
            return obj.bookmarked.filter(id=request.user.id).exists()
        return False


class ForbiddenWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForbiddenWord
        fields = [
            "word",
        ]


class SearchUserSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(source="user.name")
    nickname = serializers.SerializerMethodField(source="profile.nickname")
    last_login = serializers.StringRelatedField(source="user.last_login")

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "nickname",
            "last_login",
        ]
