from typing import Any
from django.conf import settings
from django.db import models
from django.utils import timezone
from hitcount.models import HitCountMixin

from community.models import Community
from user.models import User, Profile

import os
from uuid import uuid4


class Feed(models.Model, HitCountMixin):
    """일반 게시글 모델"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="author"
    )
    category = models.ForeignKey(
        "feed.Category",
        on_delete=models.CASCADE,
        related_name="feed_category",
        blank=False,
    )
    title = models.CharField(max_length=50)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        "user.User", blank=True, default=[], related_name="feed_likes"
    )
    is_notification = models.BooleanField(default=False)

    # 조회수 코드
    view_count = models.PositiveIntegerField(default=0)

    def click(self):
        self.view_count += 1
        self.save()

    class Meta:
        verbose_name = "일반 게시글(Feed)"
        verbose_name_plural = "일반 게시글(Feed)"


class Category(models.Model):
    """커뮤니티 내 게시글 카테고리 모델, 커뮤 생성시 기본 3개 생성"""

    community = models.ForeignKey(
        Community, on_delete=models.CASCADE, related_name="community_category"
    )
    category_name = models.CharField(max_length=20)
    category_url = models.CharField(max_length=20)

    class Meta:
        verbose_name = "커뮤니티 카테고리(Category)"
        verbose_name_plural = "커뮤니티 카테고리(Category)"

    def __str__(self):
        return self.category_name


class CommentBaseModel(models.Model):
    """댓글 기본 모델"""

    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Comment(CommentBaseModel):
    """댓글 모델"""

    feed = models.ForeignKey(Feed, related_name="comment", on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comment_author",
    )

    class Meta:
        verbose_name = "댓글(Comment)"
        verbose_name_plural = "댓글(Comment)"

    def __str__(self):
        return self.text


class Cocomment(CommentBaseModel):
    """대댓글 모델"""

    comment = models.ForeignKey(
        Comment, related_name="cocomment", on_delete=models.CASCADE, blank=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cocomment_author",
    )

    class Meta:
        verbose_name = "대댓글(Cocomment)"
        verbose_name_plural = "대댓글(Cocomment)"

    def __str__(self):
        return self.text


class GroupPurchase(models.Model, HitCountMixin):
    """공동구매 게시글 모델"""

    title = models.CharField(max_length=50)
    content = models.TextField(blank=True)
    product_name = models.CharField(max_length=20)
    product_number = models.PositiveIntegerField(default=0, help_text="구매 예상 수량")
    product_price = models.PositiveIntegerField(help_text="전체 금액")
    # product_division_price = models.PositiveIntegerField(help_text="전체 금액/구매 인원수")
    link = models.URLField(max_length=500, null=True, help_text="어떤 물건인지 링크 넣어주기")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_ended = models.BooleanField(default=False, help_text="공구 끝내기")

    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="글 작성자")
    person_limit = models.PositiveIntegerField(
        default=0, help_text="공구 제한 인원, 자기자신을 빼고 입력"
    )

    location = models.CharField(max_length=100, help_text="만날 위치")
    meeting_at = models.DateTimeField(help_text="공구 성공 후 만날 시간")
    open_at = models.DateTimeField(null=False, help_text="모집 시작")
    close_at = models.DateTimeField(null=True, help_text="모집 종료")
    END_CHOICES = (
        ("continue", "공구를 계속 진행할 거예요"),
        ("quit", "공구를 진행하지 않을 거예요"),
        ("discuss", "신청한 사람과 논의 후 결정할래요"),
        ("maybe", "종료 후 고민해보고 결정할래요"),
    )
    end_option = models.CharField(choices=END_CHOICES, max_length=20)

    community = models.ForeignKey(
        Community, on_delete=models.CASCADE, related_name="community"
    )
    category = models.ForeignKey(
        "feed.Category",
        on_delete=models.CASCADE,
        related_name="purchase_category",
        blank=False,
    )

    # 조회수 코드
    view_count = models.PositiveIntegerField(default=0)

    def get_end_option_display(self, obj):
        return dict(self.END_CHOICES).get(self.end_option)

    def click(self):
        self.view_count += 1
        self.save()

    class Meta:
        verbose_name = "공구 게시글(GroupPurchase)"
        verbose_name_plural = "공구 게시글(GroupPurchase)"

    def __str__(self):
        return f"만날 장소 : {str(self.location)} | 모집 인원 : {str(self.person_limit)}명 | 공구 물건 : {str(self.product_name)}"

    def check_end_person_limit_point(self, grouppurchase_id):
        """공구 제한 인원이 채워질 경우 공구 종료"""
        purchasefeed = GroupPurchase.objects.get(id=grouppurchase_id)
        if purchasefeed.grouppurchase is None:
            return False
        else:
            joined = purchasefeed.grouppurchase.count()
            person_count = self.person_limit - joined
            if person_count <= 0:
                self.is_ended = True
                self.save()
                return True
            else:
                return False


class GroupPurchaseComment(CommentBaseModel):
    """공구 댓글 모델"""

    grouppurchase = models.ForeignKey(
        GroupPurchase, related_name="p_comment", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="p_comment_author",
    )

    class Meta:
        verbose_name = "공구 댓글(GroupPurchaseComment)"
        verbose_name_plural = "공구 댓글(GroupPurchaseComment)"

    def __str__(self):
        return self.text


class JoinedUser(models.Model):
    """공구에 참여한 유저 모델"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="joined_user")
    grouppurchase = models.ForeignKey(
        GroupPurchase, on_delete=models.CASCADE, related_name="grouppurchase"
    )
    product_quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False, help_text="공구 참여했다가 빠진 경우")

    class Meta:
        verbose_name = "공구 지원자 현황(JoinedUser)"
        verbose_name_plural = "공구지원자 현황(JoinedUser)"

    def __str__(self):
        return f"유저 : {self.user.profile.nickname} ({self.user.profile.region}) 수량 :{self.product_quantity}"


def change_image_name(instance, filename):
    ext = os.path.splitext(filename)[-1]
    filename = "feed/BFF_%s%s" % (uuid4().hex, ext)
    return filename


class Image(models.Model):
    image = models.ImageField(upload_to=change_image_name)

    def save(self, *args, **kwargs):
        if self.image:
            new_name = change_image_name(self, self.image.name)
            self.image.name = new_name
        super(Image, self).save(*args, **kwargs)
