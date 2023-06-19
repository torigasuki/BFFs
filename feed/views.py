from rest_framework import filters, permissions, status
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from rest_framework.pagination import PageNumberPagination
from community.models import Community, CommunityAdmin
from community.serializers import CommunityAdminSerializer
from decouple import config

from feed.models import (
    Comment,
    Cocomment,
    GroupPurchaseComment,
    Feed,
    GroupPurchase,
    JoinedUser,
    Category,
    Image,
)
from feed.serializers import (
    CommentSerializer,
    CocommentSerializer,
    FeedCreateSerializer,
    FeedDetailSerializer,
    FeedListSerializer,
    FeedCreateSerializer,
    FeedNotificationSerializer,
    GroupPurchaseCreateSerializer,
    GroupPurchaseListSerializer,
    GroupPurchaseDetailSerializer,
    JoinedUserCreateSerializer,
    JoinedUserSerializer,
    GroupPurchaseCommentSerializer,
)


class CustomPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = "page_size"


class CommentView(APIView):
    # comment CUD view
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, feed_id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, feed_id=feed_id)
            return Response({"message": "댓글을 작성했습니다."}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.user != request.user:
            return Response(
                {"error": "댓글 작성자만 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN
            )
        else:
            serializer = CommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "댓글을 수정했습니다."}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.user != request.user:
            return Response(
                {"error": "댓글 작성자만 삭제할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN
            )
        else:
            comment.delete()
            return Response({"message": "댓글을 삭제했습니다."}, status=status.HTTP_200_OK)


class CocommentView(APIView):
    # 대댓글 cocomment CRUD view
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, comment_id):
        cocomment = Cocomment.objects.filter(comment_id=comment_id).order_by(
            "created_at"
        )
        if not cocomment:
            return Response({"message": "대댓글이 없습니다"}, status=status.HTTP_204_NO_CONTENT)
        else:
            serializer = CocommentSerializer(cocomment, many=True)
            return Response(
                {"message": "대댓글을 가져왔습니다", "cocomment": serializer.data},
                status=status.HTTP_200_OK,
            )

    def post(self, request, comment_id):
        serializer = CocommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, comment_id=comment_id)
            return Response({"message": "대댓글을 작성했습니다."}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, cocomment_id):
        cocomment = get_object_or_404(Cocomment, id=cocomment_id)
        if cocomment.user != request.user:
            return Response(
                {"error": "대댓글 작성자만 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN
            )
        else:
            serializer = CocommentSerializer(cocomment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "대댓글을 수정했습니다."}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, cocomment_id):
        cocomment = get_object_or_404(Cocomment, id=cocomment_id)
        if cocomment.user != request.user:
            return Response(
                {"error": "대댓글 작성자만 삭제할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN
            )
        else:
            cocomment.delete()
            return Response({"message": "대댓글을 삭제했습니다."}, status=status.HTTP_200_OK)


class FeedAllView(APIView):
    # feed 전체 리스트 view
    def get(self, request):
        feeds = Feed.objects.all().order_by("-created_at")[:3]
        serializer = FeedListSerializer(feeds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FeedListView(APIView):
    pagination_class = CustomPagination()

    # feed 전체 리스트 view
    def get(self, request, community_name):
        community = Community.objects.get(title=community_name)
        feed_list = Feed.objects.filter(category__community=community).order_by(
            "-created_at"
        )
        if not feed_list:
            return Response(
                {"message": "아직 게시글이 없습니다."}, status=status.HTTP_204_NO_CONTENT
            )
        else:
            paginated_feed_list = self.pagination_class.paginate_queryset(
                feed_list, request
            )
            serializer = FeedListSerializer(paginated_feed_list, many=True)
            pagination_serializer = self.pagination_class.get_paginated_response(
                serializer.data
            )
            return Response(pagination_serializer.data, status=status.HTTP_200_OK)


class FeedCategoryListView(APIView):
    pagination_class = CustomPagination()

    # feed 카테고리 리스트 view
    def get(self, request, community_name, category_name):
        feed_list = Feed.objects.filter(
            category__community__title=community_name,
            category__category_name=category_name,
        ).order_by("-created_at")
        if not feed_list:
            return Response(
                {"message": "아직 카테고리 게시글이 없습니다."}, status=status.HTTP_204_NO_CONTENT
            )
        else:
            paginated_feed_list = self.pagination_class.paginate_queryset(
                feed_list, request
            )
            serializer = FeedListSerializer(paginated_feed_list, many=True)
            pagination_serializer = self.pagination_class.get_paginated_response(
                serializer.data
            )
            return Response(pagination_serializer.data, status=status.HTTP_200_OK)


class FeedDetailView(APIView):
    # feed 상세보기, 수정, 삭제 view
    # 조회수 기능을 위한 모델 세팅
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    model = Feed

    # feed 상세 및 comment,cocomment 함께 가져오기
    def get(self, request, community_name, feed_id):
        # community_name이 있어야 prev, next view가 작동합니다!
        feed = get_object_or_404(Feed, id=feed_id)

        serializer = FeedDetailSerializer(feed)
        community = Category.objects.get(id=feed.category_id)
        community_title = community.community.title
        admin = Category.objects.get(id=feed.category_id).community.comu
        admin_serializer = CommunityAdminSerializer(admin, many=True)
        comment = feed.comment.all().order_by("created_at")
        feed.click
        # 댓글 유무 여부 확인
        if not comment:
            return Response(
                {
                    "message": "조회수 +1",
                    "community": community_title,
                    "feed": serializer.data,
                    "admin": admin_serializer.data,
                    "comment": "아직 댓글이 없습니다",
                },
                status=status.HTTP_200_OK,
            )
        else:
            comment_serializer = CommentSerializer(comment, many=True)
            # feed를 get할 때 조회수 올리기
            return Response(
                {
                    "message": "조회수 +1",
                    "community": community,
                    "feed": serializer.data,
                    "admin": admin_serializer.data,
                    "comment": comment_serializer.data,
                },
                status=status.HTTP_200_OK,
            )

    def put(self, request, feed_id):
        feed = get_object_or_404(Feed, id=feed_id)
        if feed.user != request.user:
            return Response(
                {"error": "게시글 작성자만 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN
            )
        else:
            serializer = FeedCreateSerializer(feed, data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response({"message": "게시글이 수정되었습니다"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, feed_id):
        feed = get_object_or_404(Feed, id=feed_id)
        if feed.user != request.user:
            return Response(
                {"error": "게시글 작성자만 삭제할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN
            )
        else:
            feed.delete()
            return Response({"message": "게시글을 삭제했습니다."}, status=status.HTTP_200_OK)


class FeedCreateView(APIView):
    # feed 생성 view
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, category_id):  # testcomu
        serializer = FeedCreateSerializer(data=request.data)
        category = get_object_or_404(Category, id=category_id)
        if serializer.is_valid():
            serializer.save(user=request.user, category=category)
            return Response({"message": "게시글이 작성되었습니다"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikeView(APIView):
    # 좋아요 기능
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, feed_id):
        feed = get_object_or_404(Feed, id=feed_id)
        if request.user in feed.likes.all():
            feed.likes.remove(request.user)
            return Response("좋아요를 취소했습니다.", status=status.HTTP_200_OK)
        else:
            feed.likes.add(request.user)
            return Response("좋아요👍를 눌렀습니다.", status=status.HTTP_200_OK)


class FeedNotificationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, community_name, feed_id):
        feed = get_object_or_404(Feed, id=feed_id)
        community = Community.objects.get(title=community_name)

        # 유저가 admin인지 확인
        user = CommunityAdmin.objects.filter(
            user=request.user, community=community
        ).last()
        if not user:
            return Response(
                {"message": "커뮤니티 관리자 권한이 없습니다"}, status=status.HTTP_403_FORBIDDEN
            )

        serializer = FeedNotificationSerializer(feed, data=request.data)
        is_notificated = serializer.post_is_notification(feed, community, request)
        serializer.is_valid(raise_exception=True)
        if is_notificated == True:
            serializer.save(is_notification=False)
            return Response(
                {"data": serializer.data, "message": "게시글 상태가 변경되었습니다"},
                status=status.HTTP_200_OK,
            )
        else:  # False일 경우
            serializer.save(is_notification=True)
            return Response(
                {"data": serializer.data, "message": "게시글 상태가 변경되었습니다"},
                status=status.HTTP_200_OK,
            )


class FeedSearchView(ListAPIView):
    search_fields = (
        "user",
        "title",
        "content",
        "created_at",
        "text",
    )
    filter_backends = filters.SearchFilter
    queryset = Feed.objects.all()
    serializer_class = FeedListSerializer, CommentSerializer


class GroupPurchaseCreateView(APIView):
    """공구 create"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, community_name):
        serializer = GroupPurchaseCreateSerializer(data=request.data)
        community = Community.objects.get(title=community_name)
        if serializer.is_valid():
            serializer.validate_datetime(request.data)
            serializer.save(community=community, user=request.user)
            return Response(
                {"message": "공동구매 게시글이 작성되었습니다"}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupPurchaseDetailView(APIView):
    """공구 detail get, update, delete"""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # 조회수 기능을 위한 모델 세팅
    model = Feed

    # feed 상세 및 comment,cocomment 함께 가져오기
    def get(self, request, community_name, grouppurchase_id):
        purchasefeed = get_object_or_404(GroupPurchase, id=grouppurchase_id)
        serializer = GroupPurchaseDetailSerializer(purchasefeed)
        purchase_comment = purchasefeed.p_comment.all().order_by("created_at")
        # 댓글 유무 여부 확인
        purchasefeed.click
        if not purchase_comment:
            return Response(
                {
                    "message": "조회수 +1",
                    "feed": serializer.data,
                    "comment": "아직 댓글이 없습니다",
                },
                status=status.HTTP_200_OK,
            )
        else:
            purchase_comment_serializer = GroupPurchaseCommentSerializer(
                purchase_comment, many=True
            )
            return Response(
                {
                    "message": "조회수 +1",
                    "grouppurchasefeed": serializer.data,
                    "comment": purchase_comment_serializer.data,
                },
                status=status.HTTP_200_OK,
            )

    def put(self, request, grouppurchase_id):
        purchasefeed = get_object_or_404(GroupPurchase, id=grouppurchase_id)
        if purchasefeed.user != request.user:
            return Response(
                {"error": "공구 게시글 작성자만 수정할 수 있습니다."}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            serializer = GroupPurchaseCreateSerializer(purchasefeed, data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(
                    {"message": "공구 게시글이 수정되었습니다"}, status=status.HTTP_200_OK
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, grouppurchase_id):
        purchasefeed = get_object_or_404(GroupPurchase, id=grouppurchase_id)
        if purchasefeed.user != request.user:
            return Response(
                {"error": "공구 게시글 작성자만 삭제할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN
            )
        else:
            print(purchasefeed.is_ended)
            if purchasefeed.is_ended == False:
                purchasefeed.delete()
                return Response(
                    {"message": "공동구매 게시글을 삭제했습니다."}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "이미 종료된 공구 게시글은 삭제할 수 없습니다"}, status=status.HTTP_
                )


class GroupPurchaseListView(APIView):
    """공구 list"""

    def get(self, request, community_name):
        community = Community.objects.get(title=community_name)
        feed_list = (
            GroupPurchase.objects.filter(community_id=community.id)
            .order_by("-created_at")
            .order_by("-is_ended")
        )
        if not feed_list:
            return Response(
                {"message": "아직 게시글이 없습니다."}, status=status.HTTP_204_NO_CONTENT
            )
        else:
            serializer = GroupPurchaseListSerializer(feed_list, many=True)
            return Response(
                {"message": "공동구매 게시글 목록을 가져왔습니다", "data": serializer.data},
                status=status.HTTP_200_OK,
            )


class GroupPurchaseJoinedUserView(APIView):
    """공구 참여 유저 생성, 수정 및 취소 view"""

    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request, grouppurchase_id):
        purchasefeed = get_object_or_404(GroupPurchase, id=grouppurchase_id)
        join_purchase = JoinedUser.objects.filter(
            user_id=request.user.id, grouppurchase_id=grouppurchase_id
        ).last()
        if not request.user.profile.region:
            return Response({"error": "유저 프로필을 업데이트 해주세요! 상세 정보가 없으면 공구를 진행할 수 없습니다."})
        if purchasefeed.check_end_person_limit_point(grouppurchase_id):
            return Response(
                {"message": "공구 인원이 모두 찼습니다!"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        if purchasefeed.is_ended == True:
            return Response(
                {"message": "이미 종료된 공구입니다!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not join_purchase and joined_user.product_quantity > 0:
            serializer = JoinedUserCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user, grouppurchase_id=grouppurchase_id)
            # save한 후 join인원 체크 및 마감여부 확인
            if purchasefeed.check_end_person_limit_point(grouppurchase_id):
                print("⭐️공구 마감⭐️")
            return Response(
                {
                    "message": "공구를 신청했습니다.",
                },
                status=status.HTTP_201_CREATED,
            )
        # True
        quantity = request.data.__getitem__("product_quantity")
        joined_user = JoinedUser.objects.get(
            user_id=request.user.id, grouppurchase_id=grouppurchase_id
        )
        serializer = JoinedUserSerializer(joined_user, data=request.data)
        if quantity < 0 or quantity == joined_user.product_quantity:
            return Response(
                {"error": "수량을 다시 확인해주세요"}, status=status.HTTP_400_BAD_REQUEST
            )
        # 수량 제한을 만들경우 필요함
        # if quantity > 남은수량:
        #     return Response({"error":"신청 수량이 남은 수량보다 많습니다."}, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer.is_valid(raise_exception=True)
        if joined_user.is_deleted is True:
            serializer.save(is_deleted=False)
            return Response(
                {"message": "공구를 재 신청했습니다.", "data": serializer.data},
                status=status.HTTP_202_ACCEPTED,
            )
        if quantity == 0:
            serializer.save(is_deleted=True)
            return Response(
                {"message": "공구 신청을 취소했습니다.", "data": serializer.data},
                status=status.HTTP_202_ACCEPTED,
            )
        if quantity != joined_user.product_quantity:
            serializer.save()
            return Response(
                {"message": "공구 수량을 수정했습니다.", "data": serializer.data},
                status=status.HTTP_202_ACCEPTED,
            )
        else:
            return Response(
                {"message": "알 수 없는 오류!", "data": serializer.data},
                status=status.HTTP_408_REQUEST_TIMEOUT,
            )


class GroupPurchaseCommentView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request, grouppurchase_id):
        serializer = GroupPurchaseCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, grouppurchase_id=grouppurchase_id)
            return Response(
                {"message": "공구 댓글을 작성했습니다."}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, purchase_comment_id):
        purchase_comment = get_object_or_404(
            GroupPurchaseComment, id=purchase_comment_id
        )
        if purchase_comment.user != request.user:
            return Response(
                {"error": "댓글 작성자만 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN
            )
        else:
            serializer = GroupPurchaseCommentSerializer(
                purchase_comment, data=request.data
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "공구 댓글을 수정했습니다."}, status=status.HTTP_200_OK
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, purchase_comment_id):
        purchase_comment = get_object_or_404(
            GroupPurchaseComment, id=purchase_comment_id
        )
        if purchase_comment.user != request.user:
            return Response(
                {"error": "댓글 작성자만 삭제할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN
            )
        else:
            purchase_comment.delete()
            return Response({"message": "공구 댓글을 삭제했습니다."}, status=status.HTTP_200_OK)


class ImageUploadAndDeleteView(APIView):
    def post(self, request):
        image = request.FILES.get("image")
        if image:
            image = Image.objects.create(image=image)
            imageurl = config("BACKEND_URL") + image.image.url
            image.delete()
            return Response(
                {"message": "이미지 업로드 성공", "image_url": imageurl},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"message": "이미지 업로드 실패"}, status=status.HTTP_400_BAD_REQUEST
            )
