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

from django.contrib.auth import get_user_model

User = get_user_model()


pytestmark = pytest.mark.django_db


class TestNewUser(TestCase):
    def setUp(self):
        self.client = APIClient()
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

    @classmethod
    def setUpTestData(cls):
        cls.danny = NewUser.objects.create_user(
            username="danny", email="danny@email.com", password="mean1234"
        )

    def test_usernames(self):
        assert self.danny.username == "danny"
        assert str(self.danny) == "danny"
        assert self.danny.is_staff == False

    def test_create_superuser(self):
        email = "admin@email.com"
        username = "admin"
        password = "1234"
        admin = User.objects.create_superuser(email, username, password)
        assert admin.is_staff == True
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_active)

        with self.assertRaises(ValueError) as exc_info:
            User.objects.create_superuser(
                email="see@email.com",
                username="see",
                password="sass",
                is_superuser=False,
            )
        # assert pytest.raises(ValueError) == True
        assert (
            str(exc_info.exception)
            == "Superuser must be assigned to is_superuser=True."
        )

        with pytest.raises(ValueError):
            User.objects.create_superuser(email, username, password, is_superuser=False)

    def test_create_superuser_error(self):
        with self.assertRaises(ValueError) as exc_info:
            User.objects.create_superuser(
                email="see@email.com",
                username="see",
                password="sass",
                is_superuser=False,
            )
        assert (
            str(exc_info.exception)
            == "Superuser must be assigned to is_superuser=True."
        )

        with pytest.raises(ValueError) as exc_info:
            # Code that raises ValueError
            User.objects.create_superuser(
                email="sees@email.com",
                username="ssee",
                password="sasss",
                is_superuser=False,
            )

            assert (
                str(exc_info.value)
                == "Superuser must be assigned to is_superuser=True."
            )

        with pytest.raises(ValueError) as exc_info:
            # Code that raises ValueError
            User.objects.create_superuser(
                email="seess@email.com",
                username="sssee",
                password="sassss",
                is_staff=False,
            )

            assert str(exc_info.value) == "Superuser must be assigned to is_staff=True."

        with pytest.raises(ValueError) as exc_info:
            # Code that raises ValueError
            User.objects.create_superuser(
                email=None,
                username="sssee",
                password="sassss",
                is_staff=False,
            )

            assert str(exc_info.value) == "You must provide an email address"

    def test_email_is_required(self):
        with pytest.raises(ValueError) as exc_info:
            User.objects.create_superuser(
                email=None, username="daneny", password="password"
            )

    def test_create_user_missing_email(self):
        User = get_user_model()
        email = None  # Missing email
        username = "user"
        password = "user123"

        with pytest.raises(ValueError) as exc_info:
            User.objects.create_user(email, username, password)

        assert str(exc_info.value) == "You must provide an email address"


def test_upload_to():
    """Test that the upload_to function returns the correct path."""

    def upload_to(instance, filename):
        return "user/{filename}".format(filename=filename)

    # Create a test instance.
    instance = {
        "filename": "test.txt",
    }

    # Call the upload_to function.
    path = upload_to(instance, filename=instance["filename"])

    # Assert that the path is correct.
    assert path == "user/test.txt"


class TestUploadTo(TestCase):
    def test_upload_to(self):
        # Create a test instance.
        instance = {
            "filename": "test.txt",
        }

        # Call the upload_to function.
        path = upload_to(instance, filename=instance["filename"])

        # Check if the path is correct.
        expected_path = "user/test.txt"
        self.assertEqual(path, expected_path)
        assert path == expected_path
