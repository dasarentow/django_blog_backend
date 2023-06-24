from django.urls import path
from .views import (
    CustomUserCreate,
    BlacklistTokenUpdateView,
    UsersView,
    RetrieveUserView,
    updateUserProfile,
    userProfile,
    userProfileUpdate,
    userProfiles,
)

app_name = "myusers"
urlpatterns = [
    path("register/", CustomUserCreate.as_view(), name="create_user"),
    path("logout/blacklist/", BlacklistTokenUpdateView.as_view(), name="blacklist"),
    # path('', UsersView.as_view()),
    path("list", UsersView.as_view(), name="list"),
    path("me", RetrieveUserView.as_view(), name="me"),
    # path('profile/', getUserProfile.as_view()),
    path("profile/update/", updateUserProfile.as_view(), name="update_user"),
    path("user/<slug:username>/", userProfiles.as_view(), name="user-profiles"),
    path("user-profile/", userProfile.as_view(), name="user-profile"),
    path("user-profile/<str:pk>/", userProfileUpdate.as_view(), name="user-profile"),
]
