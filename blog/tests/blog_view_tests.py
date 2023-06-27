import pytest
from blog.models import *
from django.test import TestCase
from django.core import serializers
from django.http import Http404
import inspect
from myusers.models import NewUser
from mixer.backend.django import mixer

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
from rest_framework.exceptions import PermissionDenied

User = get_user_model()

from model_bakery.baker import Baker


# class CustomBaker(Baker):
#     def __init__(self, _model):
#         super().__init__(_model)

#     def generate_value(self, field, commit=True):
#         if isinstance(field, AutoSlugField):
#             # Generate a unique slug value here
#             return "unique-slug-value"
#         else:
#             return super().generate_value(field, commit)


# # Use the custom baker class in your tests
# baker = CustomBaker(Category)  # Replace Category with the appropriate model

# Rest of your code...

# Rest of your code...


pytestmark = pytest.mark.django_db


# test_example.py


def add_numbers(a, b):
    return a + b


def test_add_numbers():
    result = add_numbers(2, 3)
    assert result == 5


@pytest.fixture(autouse=True)
def category_accessories():
    category = mixer.blend(Category, name="category-1")
    tag = mixer.blend(Tag, name="tag-1")
    yield category, tag
    # Clean up after the test is completed
    category.delete()
    tag.delete()


@pytest.mark.usefixtures("category_accessories")
class TestBlogViews(APITestCase):
    def setUp(self):
        self.client1 = APIClient()

        self.user1 = NewUser.objects.create_user(
            username="user1", email="user1@email.com", password="password"
        )
        self.user2 = NewUser.objects.create_user(
            username="user2", email="user2@email.com", password="password"
        )
        token_obtain_url = reverse("token_obtain_pair")
        token_refresh_url = reverse("token_refresh")
        jwt_fetch_data = {"email": "user1@email.com", "password": "password"}

        response = self.client1.post(token_obtain_url, jwt_fetch_data, format="json")
        token = response.data["access"]
        self.client1.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        category = Category.objects.get(name="category-1")

        self.post1 = mixer.blend(
            Post, title="post  1", author=self.user1, category=category
        )
        self.post2 = mixer.blend(
            Post, title="post 2", author=self.user1, category=category
        )
        self.category = Category.objects.get(name="category-1")
        self.tag = Tag.objects.get(name="tag-1")

    def test_tag_model(self):  # Add category_accessories argument
        read = Tag.objects.get(name="tag-1")
        assert read.name == "tag-1"

    def test_category_model(self):  # Add category_accessories argument
        read = Category.objects.get(name="category-1")
        assert read.name == "category-1"

    def test_post_model(self):
        assert self.post1.title == "post  1"
        assert self.post2.title == "post 2"

    def test_genereate_slug_function(self):
        instance_1 = type("Instance", (), {"title": "Hello World"})
        assert generate_slug(instance_1) == "Hello-World"

    def test_post_viewset(self):
        create_post_url = reverse("blog:post-list")
        update_post_url = reverse("blog:post-detail", kwargs={"slug": self.post1.slug})
        retrieve_post_url = reverse("blog:post-detail", args={self.post1.slug})
        # delete_post_url = reverse("blog:post-detail", args={self.post1.slug})
        delete_post_url = reverse("blog:post-detail", kwargs={"slug": self.post1.slug})

        data = {
            "category": self.category.id,
            "tag": self.tag.id,
            "content": "this is the content",
            "title": "na TITLE tHIS",
        }
        data1 = {
            "category": self.category.id,
            "tag": self.tag.id,
            "content": "this is the content",
            "title": "na title this",
        }
        create_post = self.client1.post(create_post_url, data, format="json")

        assert create_post.status_code == status.HTTP_201_CREATED
        assert create_post.data["author"]["username"] == "user1"

        """test perform_update"""
        update_post = self.client1.put(update_post_url, data1, format="json")
        assert update_post.status_code == status.HTTP_200_OK
        assert update_post.data["author"]["username"] == "user1"

        """test def retrieve()"""
        retrieve_post = self.client1.get(retrieve_post_url, data1, format="json")
        retrieve_post = self.client1.get(retrieve_post_url, data1, format="json")
        assert retrieve_post.status_code == status.HTTP_200_OK

        retrieve_post.data["views"] == 4

        client2 = APIClient()
        client2.force_authenticate(user=self.user2)

        delete_post = client2.delete(delete_post_url)
        assert delete_post.status_code == 403
        assert (
            delete_post.data["detail"]
            == "You do not have permission to perform this action."
        )
        # print(delete_post.data)

        # with pytest.raises(PermissionDenied) as exc_info:
        #     delete_post = client2.delete(delete_post_url)
        # assert str(exc_info.value) == "You don't have permission to delete this post."
        # assert (
        #     str(exc_info.exception) == "You don't have permission to delete this post."
        # )
        # print(delete_post.data)
        # self.assertEqual(
        #     str(exc_info.exception), "You don't have permission to delete this post."
        # )

        """test def add_comment(self, request, pk=None, *args, **kwargs)"""

        add_comment_url = reverse(
            "blog:post-detail-add_comment", kwargs={"slug": self.post1.slug}
        )
        data = {"content": "i am doing well", "post": self.post1.id}
        response = self.client1.post(add_comment_url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

        """ test def comment() """

        get_comment_url = reverse(
            "blog:post-comments", kwargs={"slug": self.post1.slug}
        )
        response = self.client1.get(get_comment_url, HTTP_ACCEPT="application/json")
        assert response.status_code == status.HTTP_200_OK

        # print("pot1 comments:", self.post1.comments.all().first().content)
