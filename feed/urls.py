from django.urls import path
from feed import views

urlpatterns = [
    # 개별 feed 상세, 수정 삭제
    path("<int:feed_id>/", views.FeedDetailView.as_view(), name="feed_detail_view"),
    # comment CRUD
    path("feed/<int:comment_id>/", views.FeedDetailView.as_view(), name="comment_view"),
]
