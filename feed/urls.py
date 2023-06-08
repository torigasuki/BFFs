from django.urls import path
from feed import views

urlpatterns = [
    # 개별 feed 수정 삭제
    path("<int:feed_id>/", views.FeedDetailView.as_view(), name="feed_detail_view"),
    # comment 수정 삭제
    path(
        "<int:comment_id>/", views.CommentView.as_view(), name="comment_put_delete_view"
    ),
    # cocomment 수정 삭제
    path(
        "<int:comment_id>/",
        views.CocommentView.as_view(),
        name="cocomment_put_delete_view",
    ),
    path("search/", views.FeedSearchView.as_view(), name="feed_search_view"),
]

# 이후 커뮤니티쪽에 옮길 url
urlpatterns = [
    # feed 전체 list
    path("<str:community_name>/", views.FeedListView.as_view(), name="feed_list_view"),
    # feed 카테고리 list
    path(
        "<str:community_name>/",
        views.FeedCategoryListView.as_view(),
        name="feed_category_list_view",
    ),
    # feed 생성
    path(
        "<str:community_name>/", views.FeedCreateView.as_view(), name="feed_create_view"
    ),
    # feed 상세, comment, cocoment get
    path(
        "<str:community_name>/<int:feed_id>/",
        views.FeedDetailView.as_view(),
        name="feed_detail_view",
    ),
    # comment 생성
    path(
        "<int:feed_id>/comment_id/",
        views.CommentView.as_view(),
        name="comment_create_view",
    ),
    # 대댓글, cocomment 생성
    path(
        "<int:feed_id>/comment_id/",
        views.CocommentView.as_view(),
        name="cocomment_create_view",
    ),
    # like 성공/취소
    path("<int:feed_id>/likes/", views.LikeView.as_view(), name="like_view"),
]
