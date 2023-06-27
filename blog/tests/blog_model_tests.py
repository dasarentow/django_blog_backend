import pytest
from blog.models import *
from django.test import TestCase
from django.core import serializers
from django.http import Http404
import inspect
from myusers.models import NewUser
from mixer.backend.django import mixer
import pytest
from hypothesis import given, note, strategies as st
from hypothesis.extra.django import TestCase
from rest_framework import status
from django.urls import reverse, reverse_lazy
from django.test import Client
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker
from pprint import pprint
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from urllib.parse import urlencode
from decimal import Decimal

from io import BytesIO
from PIL import Image
from decimal import Decimal
from django.core.files import File


User = get_user_model()


pytestmark = pytest.mark.django_db


@pytest.mark.django_db
def test_tag_model():
    # Create a test tag
    tag = Tag.objects.create(name="Test Tag")

    # Perform assertions to validate the model fields
    assert tag.name == "Test Tag"


@pytest.mark.django_db
def test_category_model():
    # Create a test category
    category = Category.objects.create(name="Test Category")

    # Perform assertions to validate the model fields
    assert category.name == "Test Category"


@pytest.mark.django_db
def test_post_model():
    # Create a test user
    user = User.objects.create(username="testuser")

    # Create a test category
    category = Category.objects.create(name="Test Category")

    # Create a test post
    post = Post.objects.create(
        title="Test Post",
        content="Lorem ipsum dolor sit amet.",
        author=user,
        category=category,
    )

    # Perform assertions to validate the model fields
    assert post.title == "Test Post"
    assert post.content == "Lorem ipsum dolor sit amet."
    assert post.author == user
    assert post.category == category


@pytest.mark.django_db
def test_notification_model():
    # Create a test user
    user = User.objects.create(username="testuser")

    # Create a test notification
    notification = Notification.objects.create(
        recipient=user, content="Test Notification"
    )

    # Perform assertions to validate the model fields
    assert notification.recipient == user
    assert notification.content == "Test Notification"


@pytest.mark.django_db
def test_reply_model():
    # Create a test user
    user = User.objects.create(username="testuser")

    category = Category.objects.create(name="Test Category")

    # Create a test post
    post = Post.objects.create(
        title="Test Post",
        content="Lorem ipsum dolor sit amet.",
        author=user,
        category=category,
    )
    comment = Comment.objects.create(content="Test Category", post=post, author=user)

    # Create a test reply
    reply = Reply.objects.create(author=user, content="Test Reply", comment=comment)

    # Perform assertions to validate the model fields

    assert reply.author == user
    assert reply.content == "Test Reply"


# @pytest.mark.django_db
# def test_bookmark_model():
#     # Create a test user
#     user = User.objects.create(username="testuser")

#     # Create a test post
#     post = Post.objects.create(
#         title="Test Post", content="Lorem ipsum dolor sit amet.", author=user
#     )

#     # Create a test bookmark
#     bookmark = Bookmark.objects.create(post=post, user=user)

#     # Perform assertions to validate the model fields
#     assert bookmark.post == post
#     assert bookmark.user == user


# @pytest.mark.django_db
# def test_like_model():
#     # Create a test user
#     user = User.objects.create(username="testuser")

#     # Create a test post
#     post = Post.objects.create(
#         title="Test Post", content="Lorem ipsum dolor sit amet.", author=user
#     )

#     # Create a test like
#     like = Like.objects.create(post=post, user=user)

#     # Perform assertions to validate the model fields
#     assert like.post == post
#     assert like.user == user


# @pytest.mark.django_db
# def test_comment_model():
#     # Create a test user
#     user = User.objects.create(username="testuser")

#     # Create a test category
#     category = Category.objects.create(name="Test Category")

#     # Create a test post with the category
#     post = Post.objects.create(
#         title="Test Post",
#         content="Lorem ipsum dolor sit amet.",
#         author=user,
#         category=category,
#     )

#     # Create a test comment
#     comment = Comment.objects.create(post=post, user=user, content="Test Comment")

#     # Perform assertions to validate the model fields
#     assert comment.post == post
#     assert comment.user == user
#     assert comment.content == "Test Comment"
