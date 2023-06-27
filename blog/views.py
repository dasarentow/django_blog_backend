import math
import random
from django.db.models import Max
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from requests import get
from .models import *
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db.models import F
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from django.http import Http404


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "slug"


class ReplyViewSet(ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != self.request.user:
            raise PermissionDenied("You don't have permission to update this reply.")

        return super().update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        if instance.author != self.request.user:
            raise PermissionDenied("You don't have permission to update this reply.")

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    # def perform_update(self, serializer):
    #     serializer.save(author=self.request.user)


class BookmarkViewSet(ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        post_id = self.request.data.get("post")
        get_post = get_object_or_404(Post, id=post_id)
        serializer.save(user=self.request.user, post=get_post)

    def create(self, request, *args, **kwargs):
        post_id = request.data.get("post_id")
        if not post_id:
            return Response(
                {"error": "post_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        post = Post.objects.filter(id=post_id).first()
        if not post:
            return Response(
                {"error": "Invalid post_id"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user, post=post)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer, *args, **kwargs):
        data = self.request.data
        print("data", *args, **kwargs)
        post_id = data["post"]
        print("post_id", post_id)
        content = data["content"]
        get_post = get_object_or_404(Post, id=post_id)
        # get_post = Post.objects.filter(title=post_id).first()
        serializer.save(author=self.request.user, post=get_post, content=content)

    def perform_update(self, serializer):
        author = self.request.user
        serializer.save(author=self.request.user)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "slug"
    parser_classes = (MultiPartParser, FormParser)


class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    http_method_names = ["get", "post", "delete"]

    # def perform_create(self, serializer):
    #     post = serializer.validated_data["post"]
    #     user = self.request.user

    #     # Check if the user has already liked the post
    #     if Like.objects.filter(post=post, user=user).exists():
    #         # Unlike the post if already liked
    #         Like.objects.filter(post=post, user=user).delete()
    #         raise ValidationError("Post unliked successfully.")

    #     serializer.save(user=user, post=post)
    # return Response(
    #     {"message": "post liked successfully"}, status=status.HTTP_201_CREATED
    # )
    def get_queryset(self):
        return super().get_queryset()

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)

    def perform_create(self, serializer):
        post = serializer.validated_data.get("post")
        print("mu post", post)
        user = self.request.user
        if not post:
            raise ValidationError("Post field is required.")
        if not user:
            raise ValidationError("User is not authenticated.")
        like_exists = Like.objects.filter(post=post, user=user).exists()
        if like_exists and user == user:
            Like.objects.filter(post=post, user=user).delete()
            return Response("Post unliked successfully.", status=status.HTTP_200_OK)
        else:
            serializer.save(user=user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    # @action(detail=True, methods=["post"])
    # def unlike(self, request, pk=None):
    #     like = self.get_object()

    #     # Check if the like exists
    #     if not like:
    #         return Response(
    #             {"detail": "Like not found"}, status=status.HTTP_404_NOT_FOUND
    #         )

    #     # Check if the user is the owner of the like
    #     if like.user != request.user:
    #         return Response(
    #             {"detail": "You cannot unlike a post that you did not like"},
    #             status=status.HTTP_403_FORBIDDEN,
    #         )

    #     # Delete the like
    #     like.delete()

    #     return Response(
    #         {"detail": "Post successfully unliked"}, status=status.HTTP_200_OK
    #     )


class MyLikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    http_method_names = ["get", "post"]

    def perform_create(self, serializer):
        post_id = self.request.data.get("post")
        post = Post.objects.get(id=post_id)
        serializer.save(user=self.request.user, post=post)

    @action(detail=True, methods=["post"])
    def like_unlike(self, request, pk=None):
        like = self.get_object()
        user = request.user

        # If the like exists and belongs to the requesting user
        if like and like.user == user:
            # Unlike the post
            like.delete()
            return Response(
                {"detail": "Post unliked successfully."}, status=status.HTTP_200_OK
            )
        else:
            # Like the post
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookmarkViewSet(ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    http_method_names = ["get", "post", "delete"]

    def get_queryset(self):
        return super().get_queryset()

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)

    def perform_create(self, serializer):
        post = serializer.validated_data.get("post")
        print("mu post", post)
        user = self.request.user
        if not post:
            raise ValidationError("Post field is required.")
        if not user:
            raise ValidationError("User is not authenticated.")
        bookmark_exists = Bookmark.objects.filter(post=post, user=user).exists()
        if bookmark_exists and user == user:
            Bookmark.objects.filter(post=post, user=user).delete()
            return Response("Post unliked successfully.", status=status.HTTP_200_OK)
        else:
            serializer.save(user=user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "slug"

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You don't have permission to delete this post.")
        instance.delete()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 2  # Increment the views parameter
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # Existing actions

    @action(detail=True, methods=["get"])
    def comments(self, request, pk=None, slug=None):
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post"],
        # url_path="add_comment",
    )
    def add_comment(self, request, pk=None, *args, **kwargs):
        print("heya", pk)
        data = self.request.data
        content = data.get("content")
        post = self.get_object()
        serializer = CommentSerializer(data={"content": content, "post": post.id})
        if serializer.is_valid():
            serializer.save(post=post, author=request.user, content=content)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["delete"])
    def remove_comment(self, request, pk=None):
        post = self.get_object()
        user = self.request.user

        # Retrieve the comment to be removed
        comment_id = request.data.get("comment_id")
        comment = post.comments.filter(id=comment_id).first()

        if not comment:
            return Response(
                {"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Check if the user is the author of the comment
        if comment.author != user:
            raise PermissionDenied("You don't have permission to remove this comment.")

        # Remove the comment
        comment.delete()
        return Response(
            {"detail": "Comment removed successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(detail=True, methods=["post"])
    def bookmark(self, request, pk=None):
        post = self.get_object()
        user = request.user

        # Check if the post is already bookmarked by the user
        if post.bookmarks.filter(user=user).exists():
            return Response(
                {"detail": "Post is already bookmarked."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create a new bookmark for the post
        bookmark = Bookmark(post=post, user=user)
        bookmark.save()
        return Response(
            {"detail": "Post bookmarked successfully."}, status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["delete"])
    def remove_bookmark(self, request, pk=None):
        post = self.get_object()
        user = request.user

        # Check if the post is bookmarked by the user
        bookmark = post.bookmarks.filter(user=user).first()
        if not bookmark:
            return Response(
                {"detail": "Post is not bookmarked by the user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Remove the bookmark
        bookmark.delete()
        return Response(
            {"detail": "Post bookmark removed successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )

    # Additional actions

    @action(detail=True, methods=["get"])
    def likes(self, request, pk=None):
        post = self.get_object()
        likes = post.likes.all()
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def add_like_unlike(self, request, slug=None):
        post = self.get_object()
        user = request.user

        # Check if the user has already liked the post
        likes = post.likes.filter(user=user)
        if likes.exists():
            likes.delete()
            return Response(
                {"detail": "Post unliked."},
                status=status.HTTP_200_OK,
            )

        # Create a new like for the post
        like = Like(post=post, user=user)
        like.save()
        return Response(
            {"detail": "Post liked successfully."},
        )

    @action(detail=True, methods=["delete"])
    def remove_like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        # Check if the user has liked the post
        like = post.likes.filter(user=user).first()
        if not like:
            return Response(
                {"detail": "Post is not liked by the user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Remove the like
        like.delete()
        return Response(
            {"detail": "Post like removed successfully."},
        )


@api_view(["GET", "PUT", "DELETE", "POST"])
def post_api_view(request, *args, **kwargs):
    if request.method == "GET":
        if kwargs:
            single_post = get_object_or_404(Post, slug=kwargs["slug"])
            single_post.views += 1
            single_post.save()
            serializer = PostSerializer(
                single_post, many=False, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

        qs = Post.objects.all()
        serializer = PostSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # if request.method == "POST":
    #     data = request.data


@api_view(
    [
        "GET",
        "PUT",
    ]
)
def like_and_unlike_post(request, *args, **kwargs):
    if request.method == "GET":
        queryset = Like.objects.all()
        serializer = LikeSerializer(queryset, many=True)
        return Response(serializer.data)

    if request.method == "PUT":
        user = request.user
        post = request.data["post"]
        get_post = get_object_or_404(Post, id=post)
        get_all_likes_for_post = get_post.likes.all()

        existing_like = get_all_likes_for_post.filter(user=user).first()
        if existing_like:
            existing_like.delete()
            return Response({"detail": "Post unliked successfully."}, status=200)
        else:
            like = Like.objects.create(user=request.user, post=get_post)
            serializer = LikeSerializer(like)
            return Response(serializer.data, status=201)


class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    @action(detail=False, methods=["post"])
    def mark_all_as_read(self, request):
        notifications = self.get_queryset().filter(
            recipient=request.user, is_read=False
        )
        notifications.update(is_read=True)
        return Response({"message": "All notifications marked as read."})

    @action(detail=False, methods=["get"])
    def unread_notifications(self, request):
        notifications = self.get_queryset().filter(
            recipient=request.user, is_read=False
        )
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({"message": "Notification marked as read."})

    def destroy(self, request, *args, **kwargs):
        notification = self.get_object()
        self.perform_destroy(notification)
        return Response({"message": "Notification deleted."})

    @action(detail=False, methods=["get"])
    def unread_notifications_count(self, request):
        count = (
            self.get_queryset().filter(recipient=request.user, is_read=False).count()
        )
        return Response({"count": count})


class NotificationDetailView(APIView):
    def get_object(self, notification_id):
        try:
            return Notification.objects.get(id=notification_id)
        except Notification.DoesNotExist:
            raise Http404

    def get(self, request, notification_id, format=None):
        notification = self.get_object(notification_id)
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)

    def put(self, request, notification_id, format=None):
        notification = self.get_object(notification_id)
        serializer = NotificationSerializer(notification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, notification_id, format=None):
        notification = self.get_object(notification_id)
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReplyViewSet(ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     reply = serializer.save(author=request.user)
    #     return Response(ReplySerializer(reply).data)
    def get_queryset(self):
        get_comment = get_object_or_404(Comment, id=1)
        get_reply = get_object_or_404(Reply, id=1)
        print("get_reply", get_reply.get_reply_timestamp())

        return super().get_queryset()

    def perform_create(self, serializer):
        data = self.request.data
        user = self.request.user
        comment = data["comment"]
        content = data.get("content")
        get_comment = get_object_or_404(Comment, id=comment)
        serializer.save(author=user, content=content, comment=get_comment)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        reply = serializer.save()
        return Response(ReplySerializer(reply).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)
