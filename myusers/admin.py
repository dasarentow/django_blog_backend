from django.db.models import ManyToOneRel, ForeignKey, OneToOneField
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import *


class NewUserAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'profile_pic',
                    'email', 'is_staff', 'is_active', 'is_superuser', 'password')


# Register your models here.
admin.site.register(NewUser, NewUserAccountAdmin)




# def MySpecialAdmin(model): return type('SubClass'+model.__name__, (admin.ModelAdmin,), {
#     'list_display': [x.name for x in model._meta.fields],
#     'list_select_related': [x.name for x in model._meta.fields if isinstance(x, (ManyToOneRel, ForeignKey, OneToOneField,))]
# })


# # admin.site.unregister(User)
# admin.site.register(NewUser, MySpecialAdmin(NewUser))




















# from django.contrib import admin
# from myusers.models import NewUser
# from django.contrib.auth.admin import UserAdmin
# from django.forms import TextInput, Textarea, CharField
# from django import forms
# from django.db import models


# class UserAdminConfig(UserAdmin):
#     model = NewUser
#     search_fields = ('email', 'username', 'first_name',)
#     list_filter = ('email', 'username', 'first_name', 'is_active', 'is_staff')
#     ordering = ('-start_date',)
#     list_display = ('id', 'email', 'username', 'first_name', 'about',
#                     'is_active', 'is_staff')
#     fieldsets = (
#         (None, {'fields': ('email', 'username', 'first_name',)}),
#         ('Permissions', {'fields': ('is_staff', 'is_active')}),
#         ('Personal', {'fields': ('about',)}),
#     )
#     formfield_overrides = {
#         models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
#     }
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'username', 'first_name', 'password1', 'password2', 'is_active', 'is_staff')}
#          ),
#     )


# admin.site.register(NewUser, UserAdminConfig)
