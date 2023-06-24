from django.db import models

# from django_extensions.db.fields import AutoSlugField
from django.db import models
from django.contrib.auth import get_user_model
from autoslug import AutoSlugField

User = get_user_model()

# Create your models here.


def upload_to(instance, filename):
    model_name = instance.time
    return "{model_name}/{filename}".format(model_name=model_name, filename=filename)


def generate_slug(instance):
    return instance.title.replace(" ", "-")


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(
        populate_from=("name"), max_length=100, always_update="True", unique=True
    )
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_posts(self):
        return self.posts.all()

    def get_post_count(self):
        return self.posts.count()

    def get_recent_posts(self, num_posts=5):
        return self.posts.order_by("-created_at")[:num_posts]

    @staticmethod
    def get_popular_categories(num_categories=5):
        category_ids = (
            Post.objects.values("category")
            .annotate(post_count=Count("category"))
            .order_by("-post_count")[:num_categories]
        )
        popular_categories = Category.objects.filter(
            id__in=category_ids.values_list("category", flat=True)
        )
        return popular_categories


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(
        populate_from=("name"), max_length=100, always_update="True", unique_with="name"
    )
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_posts(self):
        return self.posts.all()


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(
        populate_from=generate_slug,
        unique_with=["author", "publication_date__month"],
    )
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[("draft", "Draft"), ("published", "Published")],
        default="draft",
    )
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def increment_views(self):
        self.views += 1
        self.save()

    @staticmethod
    def get_popular_posts(num_posts=5):
        return Post.objects.order_by("-views")[:num_posts]

    def get_recent_comments(self, num_comments=5):
        return self.comments.order_by("-timestamp")[:num_comments]

    def get_comment_count(self):
        return self.comments.count()

    def get_like_count(self):
        return self.likes.count()

    def get_bookmark_count(self):
        return self.bookmarks.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = AutoSlugField(
        populate_from=("content"),
        max_length=100,
        always_update="True",
        unique_with="post__title",
    )

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

    def get_replies(self):
        return self.replies.all()

    def get_reply_count(self):
        return self.replies.count()

    def get_latest_reply(self):
        return self.replies.order_by("-timestamp").first()

    def has_replies(self):
        return self.replies.exists()

    def get_comment_author(self):
        return self.author


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Like by {self.user.username} on {self.post.title}"

    def get_liked_post(self):
        return self.post

    def get_liker(self):
        return self.user

    @staticmethod
    def has_like(user, post):
        return Like.objects.filter(user=user, post=post).exists()

    @staticmethod
    def get_like_count(post):
        return Like.objects.filter(post=post).count()

    @staticmethod
    def get_likes_by_user(user):
        return Like.objects.filter(user=user)


class Bookmark(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="bookmarks")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Bookmark by {self.user.username} on {self.post.title}"

    def get_bookmarked_post(self):
        return self.post

    def get_bookmark_user(self):
        return self.user

    @staticmethod
    def has_bookmark(user, post):
        return Bookmark.objects.filter(user=user, post=post).exists()

    @staticmethod
    def get_bookmark_count(post):
        return Bookmark.objects.filter(post=post).count()

    @staticmethod
    def get_bookmarks_by_user(user):
        return Bookmark.objects.filter(user=user)


class Notification(models.Model):
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )

    content = models.CharField(max_length=200)

    link = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.content}"

    def get_recipient(self):
        return self.recipient

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def mark_as_unread(self):
        self.is_read = False
        self.save()

    @staticmethod
    def get_unread_notifications(recipient):
        return Notification.objects.filter(recipient=recipient, is_read=False)

    @staticmethod
    def get_notification_count(recipient):
        return Notification.objects.filter(recipient=recipient).count()


class Reply(models.Model):
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="replies"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.author.username} on {self.comment.post.title}"

    def get_reply_author(self):
        return self.author

    def get_comment(self):
        return self.comment

    def get_reply_content(self):
        return self.content

    def get_reply_timestamp(self):
        return self.timestamp
