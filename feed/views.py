from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from feed.models import Feed, Comment, Cocomment

from feed.serializers import (
    FeedListSerializer,
    FeedDetailSerializer,
    FeedCreateSerializer,
    CommentSerializer,
    GroupPurchaseSerializer,
)


class CommentView(APIView):
    # comment CUD view
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # if not request.user.is_authenticated:
        #     return Response("로그인이 필요합니다.", status=status.HTTP_401_UNAUTHORIZED)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "댓글을 작성했습니다."}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.user != request.user:
            return Response(
                {"error": "댓글 작성자만 수정할 수 있습니다."}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            serializer = CommentSerializer(comment)
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


class FeedListView(APIView):
    # feed 전체 리스트 view
    def get(self, request):
        feed_list = Feed.objects.all().order_by("-created_at")
        if not feed_list:
            return Response(
                {"message": "아직 게시글이 없습니다."}, status=status.HTTP_204_NO_CONTENT
            )
        else:
            serializer = FeedListSerializer(feed_list)
            return Response(serializer.data, status=status.HTTP_200_OK)


class FeedCategoryListView(APIView):
    # feed 카테고리 리스트 view
    def get(self, request, category_name):
        feed_list = Feed.objects.filter(category_name=category_name)
        if not feed_list:
            return Response(
                {"message": "아직 게시글이 없습니다."}, status=status.HTTP_204_NO_CONTENT
            )
        else:
            serializer = FeedListSerializer(feed_list)
            return Response(serializer.data, status=status.HTTP_200_OK)


class FeedDetailView(APIView):
    # feed 상세보기, 수정, 삭제 view
    # 조회수 기능을 위한 모델 세팅
    model = Feed
    permission_classes = [permissions.IsAuthenticated]

    # feed 상세 및 comment,cocomment 함께 가져오기
    def get(self, request, feed_id):
        feed = get_object_or_404(Feed, id=feed_id)
        serializer = FeedDetailSerializer(feed)
        comment = feed.comment.all().order_by("created_at")
        # 댓글 유무 여부 확인
        if not comment:
            return Response(
                {
                    "message": "조회수 +1",
                    "feed": serializer.data,
                    "comment": "아직 댓글이 없습니다",
                },
                status=status.HTTP_200_OK,
            )
        else:
            comment_serializer = CommentSerializer(comment, many=True)
            # feed를 get할 때 조회수 올리기
            feed.click
            return Response(
                {
                    "message": "조회수 +1",
                    "feed": serializer.data,
                    "comment": comment_serializer.data,
                },
                status=status.HTTP_200_OK,
            )

    # feed 조회수 기능 => get할때 조회수가 올라가도록 바꾸기! 작동 확인 후 주석 및 코드 삭제하도록 하겠음
    # def post(self, request, feed_id):
    #     feed = get_object_or_404(Feed, id=feed_id)
    #     feed.click
    #     return Response("조회수 +1", status=status.HTTP_200_OK)

    def put(self, request, feed_id):
        # if not request.user.is_authenticated:
        #     return Response("로그인이 필요합니다.", status=status.HTTP_401_UNAUTHORIZED)
        feed = get_object_or_404(Feed, id=feed_id)
        if feed.user != request.user:
            return Response(
                {"error": "게시글 작성자만 수정할 수 있습니다."}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            serializer = FeedCreateSerializer(feed)
            if serializer.is_valid:
                serializer.save()
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
    def post(self, request):
        if not request.user.is_authenticated:
            return Response("로그인이 필요합니다.", status=status.HTTP_401_UNAUTHORIZED)
        serializer = FeedCreateSerializer(data=request.data)
        if serializer.is_valid:
            serializer.save(user=request.user)
            return Response({"message": "게시글이 작성되었습니다"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
