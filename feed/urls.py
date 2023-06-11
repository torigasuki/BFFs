from django.urls import path
from feed import views

urlpatterns = [
    # 개별 feed 수정 삭제
    path("<int:feed_id>/", views.FeedDetailView.as_view(), name="feed_detail_view"),
    # feed 생성
    path(
        "<str:community_name>/feed/",
        views.FeedCreateView.as_view(),
        name="feed_create_view",
    ),
    # comment 생성
    path(
        "<int:feed_id>/comment/",
        views.CommentView.as_view(),
        name="comment_create_view",
    ),
    # comment 수정 삭제
    path(
        "comment/<int:comment_id>/",
        views.CommentView.as_view(),
        name="comment_put_delete_view",
    ),
    # 대댓글, cocomment get 생성
    path(
        "<int:comment_id>/cocomment/",
        views.CocommentView.as_view(),
        name="cocomment_create_view",
    ),
    # cocomment 수정 삭제
    path(
        "cocomment/<int:cocomment_id>/",
        views.CocommentView.as_view(),
        name="cocomment_put_delete_view",
    ),
    # grouppurchase 게시글 생성
    path(
        "<str:community_name>/grouppurchase/",
        views.GroupPurchaseCreateView.as_view(),
        name="grouppurchase_create_view",
    ),
    # grouppurchase 게시글 수정 삭제
    path(
        "grouppurchase/<int:grouppurchase_id>/",
        views.GroupPurchaseDetailView.as_view(),
        name="grouppurchase_put_delete_view",
    ),
    # grouppurchase 참여 / 취소
    path(
        "<int:grouppurchase_id>/join/",
        views.GroupPurchaseJoinedUserView.as_view(),
        name="grouppurchase_join_view",
    ),
]
