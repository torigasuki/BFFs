from django.urls import path
from .views import (
    FeedSearchView,
    FeedAllView,
    CommentView,
    CommentView,
    CocommentView,
    CocommentView,
    GroupPurchaseCommentView,
    ImageUploadAndDeleteView,
    FeedNotificationView,
    LikeView,
)

urlpatterns = [
    # feed 검색
    path("search", FeedSearchView.as_view(), name="search_community_view"),
    # 랜덤 커뮤 인기 feed list 조회
    path("", FeedAllView.as_view(), name="feed_view"),
    # like 설정/취소
    path("<int:feed_id>/likes/", LikeView.as_view(), name="like_view"),
    # feed 게시글 공지 설정/취소
    path(
        "<int:feed_id>/notification/",
        FeedNotificationView.as_view(),
        name="feed_notification_view",
    ),
    # comment 생성
    path(
        "<int:feed_id>/comment/",
        CommentView.as_view(),
        name="comment_create_view",
    ),
    # comment 수정 삭제
    path(
        "comment/<int:comment_id>/",
        CommentView.as_view(),
        name="comment_put_delete_view",
    ),
    # 대댓글, cocomment get 생성
    path(
        "<int:comment_id>/cocomment/",
        CocommentView.as_view(),
        name="cocomment_create_view",
    ),
    # cocomment 수정 삭제
    path(
        "cocomment/<int:cocomment_id>/",
        CocommentView.as_view(),
        name="cocomment_put_delete_view",
    ),
    # grouppurchase comment 수정 삭제
    path(
        "purchasecomment/<int:purchase_comment_id>/",
        GroupPurchaseCommentView.as_view(),
        name="purchase_comment_put_delete_view",
    ),
    path("image/upload/", ImageUploadAndDeleteView.as_view(), name="image_upload_view"),
]
