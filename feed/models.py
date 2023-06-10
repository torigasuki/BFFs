from django.db import models
from hitcount.models import HitCountMixin, HitCount
from django.conf import settings
from user.models import User
from community.models import Community
from user.models import Profile
from django.utils import timezone


# 일반 feed 모델
class Feed(models.Model, HitCountMixin):
    community = models.ForeignKey(
        Community, on_delete=models.CASCADE, related_name="community_feeds"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="author"
    )
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to="media/photo/%Y/%m/%d", null=True, blank=True)
    video = models.FileField(upload_to="media/video/%Y/%m/%d", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        "user.User", blank=True, default=[], related_name="feed_likes"
    )
    is_notification = models.BooleanField(default=False)

    category = models.ManyToManyField(
        "feed.Category", related_name="feed_category", blank=False
    )

    # 조회수 코드
    view_count = models.PositiveIntegerField(default=0)

    @property
    def click(self):
        self.view_count += 1
        self.save()


# community 내 feed에 대한 카테고리 모델, 전체/자유/모집/공구
class Category(models.Model):
    category_name = models.CharField(max_length=20)

    def __str__(self):
        return self.category_name


# 댓글 모델
class Comment(models.Model):
    feed = models.ForeignKey(Feed, related_name="comment", on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comment_author",
    )
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


# 대댓글 모델
class Cocomment(models.Model):
    comment = models.ForeignKey(
        Comment, related_name="cocomment", on_delete=models.CASCADE, blank=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cocomment_author",
    )
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


# 공구 게시글
class GroupPurchase(models.Model, HitCountMixin):
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True)
    product_name = models.CharField(max_length=50)
    product_number = models.PositiveIntegerField(default=0, help_text="구매 예상 수량")
    link = models.CharField(max_length=300, help_text="어떤 물건인지 링크 넣어주기")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_ended = models.BooleanField(default=False)

    userprofile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, help_text="글 작성자"
    )
    person_count = models.PositiveIntegerField(default=0, help_text="공구 제한 인원")

    location = models.CharField(max_length=100, help_text="만날 위치")
    meeting_at = models.DateTimeField(help_text="공구 성공 후 만날 시간")
    open_at = models.DateTimeField(null=False, help_text="모집 시작")
    close_at = models.DateTimeField(null=True, help_text="모집 종료")
    END_CHOICES = (
        ("continue", "공구를 계속 진행할 거예요"),
        ("quit", "공구를 진행 하지 않을 거예요"),
        ("discuss", "신청한 사람과 논의 후 결정할래요"),
        ("maybe", "종료 후 고민해보고 결정할래요"),
    )
    end_option = models.CharField(choices=END_CHOICES, max_length=8)

    community = models.ForeignKey(
        Community, on_delete=models.CASCADE, related_name="community_purchases"
    )
    category = models.ManyToManyField(
        "feed.Category", related_name="purchase_category", blank=False, default="공구해요"
    )

    # 조회수 코드
    view_count = models.PositiveIntegerField(default=0)

    @property
    def click(self):
        self.view_count += 1
        self.save()

    def __str__(self):
        return f"만날 장소 : {str(self.location)} | 모집 인원 : {str(self.person_count)}명 | 공구 물건 : {str(self.product_name)}"


# 공구에 참여한 유저 모델
class JoinedUser(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    grouppurchase = models.ForeignKey(GroupPurchase, on_delete=models.CASCADE)

    select_purchase = models.ManyToManyField("self", blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_joined = models.BooleanField(default=False, help_text="공구 참여 여부")
    already_joined = models.IntegerField(null=True, blank=True, help_text="참여한 공구")

    class Meta:
        verbose_name = "미팅지원자 현황(JoinedUser)"
        verbose_name_plural = "미팅지원자 현황(JoinedUser)"

    def __str__(self):
        return f"실명 :{self.profile.user.name} ({self.profile.region})"
