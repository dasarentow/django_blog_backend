from django.test import TestCase
from myusers.models import NewUser, upload_to
from mixer.backend.django import mixer
import pytest
from hypothesis import given, note, strategies as st
from hypothesis.extra.django import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from model_bakery import baker
from pprint import pprint
from myusers.views import userProfile
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from rest_framework_simplejwt.tokens import RefreshToken


from django.contrib.auth import get_user_model

User = get_user_model()


pytestmark = pytest.mark.django_db


class CustomUserCreateTestCase(APITestCase):
    def test_create_user(self):
        url = reverse("myusers:create_user")
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "testuser")
        assert response.data["email"] == "testuser@example.com"

    def test_error_in_create_user(self):
        url = reverse("myusers:create_user")
        data = {
            "username": "testusers",
            "email": "testusere",
            "password": "testpassword",
        }
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestBlacklistTokenUpdateView(APITestCase):
    def test_blacklist_token(self):
        """Test that the BlacklistTokenUpdateView view can blacklist a token."""

        # Create a user.
        user = User.objects.create_user(
            username="test_user",
            email="test_user@example.com",
            password="password",
        )

        # Create a refresh token for the user.
        refresh_token = RefreshToken.for_user(user)

        # Blacklist the token.
        refresh = refresh_token
        access = refresh_token.access_token
        url = reverse("myusers:blacklist")

        response = self.client.post(
            url,
            data={"refresh_token": str(refresh_token)},
            format="json",
        )

        # Assert that the response is a 205 Reset Content response.

        assert response.status_code == status.HTTP_205_RESET_CONTENT

        # # Assert that the token is blacklisted.
        # token = RefreshToken(refresh_token.access_token)

        test_blacklist = self.client.post(
            url,
            data={"refresh_token": "simulating bad refresh token"},
            format="json",
        )
        assert test_blacklist.status_code == status.HTTP_400_BAD_REQUEST
        # assert token.is_blacklisted()


class TestRetrieveUserAPIView(APITestCase):
    def setUp(self):
        # self.client = APIClient()
        username = "testuser"
        email = "testuser@email.com"
        password = "testpassword"

        self.new_user = NewUser.objects.create_user(
            username=username, email=email, password=password
        )
        jwt_fetch_data = {"email": email, "password": password}
        token_obtain_url = reverse("token_obtain_pair")
        token_refresh_url = reverse("token_refresh")
        response = self.client.post(token_obtain_url, jwt_fetch_data, format="json")
        token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        self.factory = APIRequestFactory()

    def test_retrieve_user_me(self):
        url = reverse("myusers:me")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_users_view(self):
        username = "testsuser"
        email = "testuswer@email.com"
        password = "testpassword"

        self.new_user = NewUser.objects.create_superuser(
            username=username, email=email, password=password
        )
        jwt_fetch_data = {"email": email, "password": password}
        token_obtain_url = reverse("token_obtain_pair")
        token_refresh_url = reverse("token_refresh")
        response = self.client.post(token_obtain_url, jwt_fetch_data, format="json")
        token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        url = reverse("myusers:list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_user_profile(self):
        url = reverse(
            "myusers:user-profiles", kwargs={"username": self.new_user.username}
        )
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert data["email"] == self.new_user.email
        user = self.new_user.email
        assert self.new_user.email == data["email"]
        assert NewUser.objects.get(email=self.new_user.email) == self.new_user
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "testuser@email.com")

    def test_retrieve_update_view(self):
        url = reverse("myusers:user-profile", kwargs={"pk": self.new_user.pk})
        response = self.client.get(url)
        data = response.data

        assert self.new_user.email == data["email"]

        data = {
            "username": self.new_user.username,
        }
        response = self.client.put(url, data, format="json")
        assert self.new_user.username == data["username"]

    def test_profile(self):
        url = reverse("myusers:update_user")
        data = {
            "username": self.new_user.username,
        }
        response = self.client.put(url, data, content="application/json")
        data = response.data
        assert response.status_code == status.HTTP_200_OK

        data = {
            "usernamesds": self.new_user.username,
        }
        response = self.client.put(url, data, content="application/json")
        data = response.data
        assert response.status_code == status.HTTP_400_BAD_REQUEST
