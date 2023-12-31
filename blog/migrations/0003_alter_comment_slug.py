# Generated by Django 4.2.2 on 2023-06-24 03:44

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0002_comment_slug_notification_is_read"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="slug",
            field=autoslug.fields.AutoSlugField(
                always_update="True",
                editable=False,
                max_length=100,
                populate_from=("post.title", "author.username", "content"),
                unique_with=("post__title",),
            ),
        ),
    ]
