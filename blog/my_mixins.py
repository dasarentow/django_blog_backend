from django.db import models
from django.contrib.auth import get_user_model
from blog.models import *
from datetime import datetime

User = get_user_model()

# Define the mixins


class SlugMixin(models.Model):
    slug = models.SlugField(unique=True)

    def generate_slug(self):
        return self.title.replace(" ", "-")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class AuthorMixin(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class ViewCountMixin(models.Model):
    views = models.PositiveIntegerField(default=0)

    def increment_views(self):
        self.views += 1
        self.save(update_fields=["views"])

    class Meta:
        abstract = True


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TaggableMixin(models.Model):
    tags = models.ManyToManyField(Tag)

    def add_tag(self, tag):
        self.tags.add(tag)

    def remove_tag(self, tag):
        self.tags.remove(tag)

    def get_tags(self):
        return self.tags.all()


class CommentableMixin(models.Model):
    comments = models.ManyToManyField(Comment)

    def add_comment(self, comment):
        self.comments.add(comment)

    def delete_comment(self, comment):
        self.comments.remove(comment)

    def get_comments(self):
        return self.comments.all()


class LikeableMixin(models.Model):
    likes = models.ManyToManyField(User, related_name="%(class)s_likes")

    def add_like(self, user):
        self.likes.add(user)

    def remove_like(self, user):
        self.likes.remove(user)

    def get_likes(self):
        return self.likes.all()


class PublishableMixin(models.Model):
    is_published = models.BooleanField(default=False)
    publish_date = models.DateTimeField(null=True, blank=True)

    def publish(self):
        self.is_published = True
        self.publish_date = datetime.now()
        self.save()

    def unpublish(self):
        self.is_published = False
        self.publish_date = None
        self.save()

    def schedule_publish(self, publish_date):
        self.is_published = False
        self.publish_date = publish_date
        self.save()
