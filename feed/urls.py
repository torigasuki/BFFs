from django.urls import path
from .views import (
    FeedSearchView,
    FeedListView,
    FeedCreateView,
    FeedDetailView,
    FeedCategoryListView,
    CommentView,
    CocommentView,
    GroupPurchaseListView,
    GroupPurchaseCreateView,
    GroupPurchaseDetailView,
    GroupPurchaseJoinedUserView,
    GroupPurchaseSelfEndView,
    GroupPurchaseCommentView,
    ImageUploadAndDeleteView,
    FeedNotificationView,
    LikeView,
)

urlpatterns = [
    # feed 검색
    path("search", FeedSearchView.as_view(), name="search_feed_view"),
    # feed 카테고리 list get
    path(
        "category/<str:category_url>/",
        FeedCategoryListView.as_view(),
        name="feed_category_list_view",
    ),
    # feed 전체 list get
    path(
        "list/",
        FeedListView.as_view(),
        name="feed_list_view",
    ),
    # feed 생성
    path("feed/", FeedCreateView.as_view(), name="feed_create_view"),
    # feed 상세, comment get / 수정 삭제
    path(
        "feed/<int:feed_id>/",
        FeedDetailView.as_view(),
        name="feed_detail_view",
    ),
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
    # grouppurchase 전체 list
    path(
        "grouppurchase/list/",
        GroupPurchaseListView.as_view(),
        name="grouppurchase_list_view",
    ),
    # grouppurchase 게시글 생성
    path(
        "grouppurchase/",
        GroupPurchaseCreateView.as_view(),
        name="grouppurchase_create_view",
    ),
    # grouppurchase 상세 페이지 / 수정 삭제
    path(
        "grouppurchase/<int:grouppurchase_id>/",
        GroupPurchaseDetailView.as_view(),
        name="grouppurchase_detail_view",
    ),
    # grouppurchase 참여 / 취소
    path(
        "grouppurchase/<int:grouppurchase_id>/join/",
        GroupPurchaseJoinedUserView.as_view(),
        name="grouppurchase_join_view",
    ),
    # grouppurchase 작성자 모집 끝 옵션
    path(
        "grouppurchase/<int:grouppurchase_id>/self_end/",
        GroupPurchaseSelfEndView.as_view(),
        name="purchase_self_end_view",
    ),
    # grouppurchase comment 생성
    path(
        "grouppurchase/<int:grouppurchase_id>/purchasecomment/",
        GroupPurchaseCommentView.as_view(),
        name="purchase_comment_create_view",
    ),
    # grouppurchase comment 수정 삭제
    path(
        "purchasecomment/<int:purchase_comment_id>/",
        GroupPurchaseCommentView.as_view(),
        name="purchase_comment_put_delete_view",
    ),
    path("image/upload/", ImageUploadAndDeleteView.as_view(), name="image_upload_view"),
    # 랜덤 커뮤 인기 feed list 조회
    # path("", FeedAllView.as_view(), name="feed_view"),
]
