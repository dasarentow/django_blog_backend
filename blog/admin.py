from django.contrib import admin

# Register your models here.
from django.contrib import admin

from django.db.models import ManyToOneRel, ForeignKey, OneToOneField


# Register your models here.

from .models import *


def MySpecialAdmin(model):
    return type(
        "SubClass" + model.__name__,
        (admin.ModelAdmin,),
        {
            "list_display": [x.name for x in model._meta.fields],
            "list_select_related": [
                x.name
                for x in model._meta.fields
                if isinstance(
                    x,
                    (
                        ManyToOneRel,
                        ForeignKey,
                        OneToOneField,
                    ),
                )
            ],
        },
    )


class TagAdmin(admin.ModelAdmin):
    list_display = [x.name for x in Tag._meta.fields]


class CategoryAdmin(admin.ModelAdmin):
    list_display = [x.name for x in Category._meta.fields]


class CommentAdmin(admin.ModelAdmin):
    list_display = [x.name for x in Comment._meta.fields]


class LikeAdmin(admin.ModelAdmin):
    list_display = [x.name for x in Like._meta.fields]


class BookmarkAdmin(admin.ModelAdmin):
    list_display = [x.name for x in Bookmark._meta.fields]


class PostAdmin(admin.ModelAdmin):
    list_display = [x.name for x in Post._meta.fields]

    def get_readonly_fields(self, request, obj=None):
        # Make 'is_editors_pick' field readonly for non-superusers
        if not request.user.is_superuser:
            return ("is_editors_pick",)
        return ()


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Bookmark, BookmarkAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(Reply)
admin.site.register(Post, PostAdmin)
