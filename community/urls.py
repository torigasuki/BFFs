from django.urls import path, include
from .views import (
    CommunityView,
    CommunityDetailView,
    CommunitySubAdminView,
    CommunityForbiddenView,
    CommunityBookmarkView,
    SearchCommunityView,
    CommunityCategoryView,
    FeedNextView,
    FeedPrevView,
)
from feed.views import (
    FeedListView,
    FeedCategoryListView,
    FeedCreateView,
    FeedDetailView,
    GroupPurchaseListView,
    GroupPurchaseCreateView,
    GroupPurchaseDetailView,
    GroupPurchaseJoinedUserView,
    GroupPurchaseSelfEndView,
    GroupPurchaseCommentView,
)

urlpatterns = [
    path("", CommunityView.as_view(), name="community_view"),
    path("<str:community_url>/feed/", include("feed.urls")),
    path(
        "<str:community_url>/",
        CommunityDetailView.as_view(),
        name="community_detail_view",
    ),
    path(
        "<str:community_url>/category/",
        CommunityCategoryView.as_view(),
        name="community_category_view",
    ),
    path(
        "<str:community_url>/subadmin/",
        CommunitySubAdminView.as_view(),
        name="community_subadmin_view",
    ),
    path(
        "<str:community_url>/forbidden/",
        CommunityForbiddenView.as_view(),
        name="community_forbidden_view",
    ),
    path(
        "<str:community_url>/forbidden/<str:forbidden_word>/",
        CommunityForbiddenView.as_view(),
        name="community_forbidden_view",
    ),
    path(
        "<str:community_url>/bookmark/",
        CommunityBookmarkView.as_view(),
        name="community_bookmark_view",
    ),
    path("search", SearchCommunityView.as_view(), name="search_community_view"),
    # feed 전체 list get
    path(
        "<str:community_url>/list/",
        FeedListView.as_view(),
        name="feed_list_view",
    ),
    # feed 카테고리 list get
    path(
        "<str:community_url>/category/<str:category_url>/",
        FeedCategoryListView.as_view(),
        name="feed_category_list_view",
    ),
    # feed 생성
    path(
        "<str:community_url>/feed/",
        FeedCreateView.as_view(),
        name="feed_create_view",
    ),
    # feed 상세, comment get / 수정 삭제
    path(
        "<str:community_url>/feed/<int:feed_id>/",
        FeedDetailView.as_view(),
        name="feed_detail_view",
    ),
    # 이전 글, 다음 글
    path(
        "<str:community_url>/feed/<int:feed_id>/prev/",
        FeedPrevView.as_view(),
        name="prev_feed",
    ),
    path(
        "<str:community_url>/feed/<int:feed_id>/next/",
        FeedNextView.as_view(),
        name="next_feed",
    ),
    # grouppurchase 전체 list
    path(
        "<str:community_url>/grouppurchase/list/",
        GroupPurchaseListView.as_view(),
        name="grouppurchase_list_view",
    ),
    # grouppurchase 게시글 생성
    path(
        "<str:community_url>/grouppurchase/",
        GroupPurchaseCreateView.as_view(),
        name="grouppurchase_create_view",
    ),
    # grouppurchase 상세 페이지 / 수정 삭제
    path(
        "<str:community_url>/grouppurchase/<int:grouppurchase_id>/",
        GroupPurchaseDetailView.as_view(),
        name="grouppurchase_detail_view",
    ),
    # grouppurchase 참여 / 취소
    path(
        "<str:community_url>/grouppurchase/<int:grouppurchase_id>/join/",
        GroupPurchaseJoinedUserView.as_view(),
        name="grouppurchase_join_view",
    ),
    # grouppurchase 작성자 모집 끝 옵션
    path(
        "<str:community_url>/grouppurchase/<int:grouppurchase_id>/self_end/",
        GroupPurchaseSelfEndView.as_view(),
        name="purchase_self_end_view",
    ),
    # grouppurchase comment 생성
    path(
        "<str:community_url>/grouppurchase/<int:grouppurchase_id>/purchasecomment/",
        GroupPurchaseCommentView.as_view(),
        name="purchase_comment_create_view",
    ),
]
