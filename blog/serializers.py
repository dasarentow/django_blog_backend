from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from myusers.serializers import *
from .models import *
from drf_writable_nested.serializers import WritableNestedModelSerializer
from myusers.serializers import UserPublicSerializer
from rest_framework import viewsets, permissions


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description"]
        read_only_fields = ("slug", "id")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug", "description"]
        read_only_fields = ["slug"]


class PostSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(many=False, read_only=True)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "content",
            "publication_date",
            "author",
            "category",
            "image",
            "status",
            "views",
            "is_editors_pick",
        ]
        read_only_fields = ("views", "publication_date", "slug", "author")


class CommentSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(many=False, read_only=True)
    post = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=Post.objects.all(),
    )

    class Meta:
        model = Comment
        fields = ("id", "post", "author", "content", "timestamp")
        read_only_fields = (
            "id ",
            "author",
            "timestamp",
            "slug",
        )

    # def create(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         user = request.user
    #         request.data['user'] = user.id
    #     else:
    #         user = None
    #         request.data['user'] = None

    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     if user:
    #         serializer.validated_data['name'] = user.username
    #     else:
    #         serializer.validated_data['name'] = 'Anonymous'

    #     self.perform_create(serializer)

    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def create(self, validated_data):
    #     post_data = validated_data.pop("post")  # Extract the nested post data
    #     post_serializer = PostSerializer(data=post_data)
    #     post_serializer.is_valid(raise_exception=True)
    #     post_instance = post_serializer.save()  # Save the nested post instance

    #     # Create the comment object with the nested post instance
    #     comment = Comment.objects.create(post=post_instance, **validated_data)
    #     return comment

    # def update(self, instance, validated_data):
    #     if "post" in validated_data:
    #         post_data = validated_data.pop("post")  # Extract the nested post data
    #         post_serializer = PostSerializer(instance.post, data=post_data)
    #         post_serializer.is_valid(raise_exception=True)
    #         post_instance = (
    #             post_serializer.save()
    #         )  # Save the updated nested post instance
    #         instance.post = post_instance

    #     # Update the remaining fields of the comment instance
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     return instance


class LikeSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(many=False, read_only=True)
    post = serializers.PrimaryKeyRelatedField(many=False, queryset=Post.objects.all())

    class Meta:
        model = Like
        fields = ["post", "user"]
        read_only_fields = ["user"]


class NotificationSerializer(serializers.ModelSerializer):
    recipient = UserPublicSerializer(many=False, read_only=True)

    class Meta:
        model = Notification
        fields = ["id", "recipient", "content", "link", "timestamp"]
        read_only_fields = ["recipient"]


class ReplySerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(many=False, read_only=True)
    comment = serializers.PrimaryKeyRelatedField(
        many=False, queryset=Comment.objects.all()
    )

    class Meta:
        model = Reply
        fields = ["id", "comment", "author", "content", "timestamp"]
        read_only_fields = ["author", "timestamp"]


class BookmarkSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(many=False, read_only=True)
    post = serializers.PrimaryKeyRelatedField(many=False, queryset=Post.objects.all())

    class Meta:
        model = Bookmark
        fields = ["id", "post", "user"]
        read_only_fields = ["user"]
