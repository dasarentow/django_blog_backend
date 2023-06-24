from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"tag", TagViewSet, basename="tag")
router.register(r"Category", CategoryViewSet, basename="category")
router.register(r"notification", NotificationViewSet, basename="notification")
router.register(r"reply", ReplyViewSet, basename="reply")
router.register(r"bookmark", BookmarkViewSet, basename="bookmark")
router.register(r"like", LikeViewSet, basename="like")
router.register(r"likes", MyLikeViewSet, basename="likes")
router.register(r"comment", CommentViewSet, basename="comment")
router.register(r"posts", PostViewSet, basename="post")

app_name = "blog"
urlpatterns = [
    path("post_api_view/", post_api_view, name="post_api_view"),
    path("post_api_view/<slug:slug>/", post_api_view, name="post_api_view"),
    path("like_and_unlike/", like_and_unlike_post, name="like_and_unlike"),
    path("", include(router.urls)),
]

"""
GET /posts/: Retrieves a list of all posts.
POST /posts/: Creates a new post.
GET /posts/{slug}/: Retrieves details of a specific post.
PUT /posts/{slug}/: Updates a specific post.
PATCH /posts/{slug}/: Partially updates a specific post.
DELETE /posts/{slug}/: Deletes a specific post.
GET /posts/{slug}/comments/: Retrieves all comments for a specific post.
POST /posts/{slug}/add_comment/: Adds a comment to a specific post.
POST /posts/{slug}/bookmark/: Adds a bookmark to a specific post.
DELETE /posts/{slug}/remove_bookmark/: Removes a bookmark from a specific post.
GET /posts/{slug}/likes/: Retrieves all likes for a specific post.
POST /posts/{slug}/add_like/: Adds a like to a specific post.
DELETE /posts/{slug}/remove_like/: Removes a like from a specific post.
"""


"""
^posts/$ [name='post-list']
^posts/{slug}/$ [name='post-detail']
^posts/{slug}/comments/$ [name='post-comments']
^posts/{slug}/comments/add_comment/$ [name='post-add-comment']
^posts/{slug}/bookmark/$ [name='post-bookmark']
^posts/{slug}/remove_bookmark/$ [name='post-remove-bookmark']
^posts/{slug}/likes/$ [name='post-likes']
^posts/{slug}/add_like/$ [name='post-add-like']
^posts/{slug}/remove_like/$ [name='post-remove-like']

"""

"""
path('posts/<slug:slug>/comments/', PostViewSet.as_view({'get': 'comments'}), name='post-comments'),
    path('posts/<slug:slug>/comments/add_comment/', PostViewSet.as_view({'post': 'add_comment'}), name='post-add-comment'),
    path('posts/<slug:slug>/bookmark/', PostViewSet.as_view({'post': 'bookmark'}), name='post-bookmark'),
    path('posts/<slug:slug>/remove_bookmark/', PostViewSet.as_view({'post': 'remove_bookmark'}), name='post-remove-bookmark'),
    path('posts/<slug:slug>/likes/', PostViewSet.as_view({'get': 'likes'}), name='post-likes'),
    path('posts/<slug:slug>/add_like/', PostViewSet.as_view({'post': 'add_like'}), name='post-add-like'),
    path('posts/<slug:slug>/remove_like/', PostViewSet.as_view({'post': 'remove_like'}), name='post-remove-like'),

"""

"""
PostViewSet

^posts/$ [name='post-list']
^posts/{pk}/$ [name='post-detail']
^posts/{pk}/comments/$ [name='post-comments']
^posts/{pk}/comments/add_comment/$ [name='post-add-comment']
^posts/{pk}/bookmark/$ [name='post-bookmark']
^posts/{pk}/remove_bookmark/$ [name='post-remove-bookmark']
^posts/{pk}/likes/$ [name='post-likes']
^posts/{pk}/add_like/$ [name='post-add-like']
^posts/{pk}/remove_like/$ [name='post-remove-like']


"""

"""
MyLikeViewSet
GET /likes/ - Retrieve a list of likes
POST /likes/ - Create a new like
GET /likes/{pk}/ - Retrieve a specific like
PUT /likes/{pk}/ - Update a specific like
PATCH /likes/{pk}/ - Partially update a specific like
DELETE /likes/{pk}/ - Delete a specific like
POST /likes/{pk}/like_unlike/ - Like or unlike a post (custom action)


"""
