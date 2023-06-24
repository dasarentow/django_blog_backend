
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
