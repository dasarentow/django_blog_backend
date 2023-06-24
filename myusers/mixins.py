# from .permissions import IsStaffEditorPermission
# from rest_framework import permissions
# from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth.models import Group
# import logging


# class StaffEditorPermissionMixin:
#     permission_classes = [
#         permissions.IsAdminUser,
#         IsAuthenticated,
#         IsStaffEditorPermission,
#     ]


# class UserQuerySetMixin:
#     user_field = "user"
#     allow_staff_view = False

#     def get_queryset(self, request, *args, **kwargs):
#         user = self.request.user
#         lookup_data = {}
#         # lookup_data[self.user_field] = self.request.user
#         lookup_data[self.user_field] = user
#         print("lookie", lookup_data)
#         logging.debug("Lookup Data: %s", lookup_data)
#         qs = super().get_queryset(*args, **kwargs)
#         if self.allow_staff_view and user.is_staff:
#             # if user.is_staff:
#             return qs
#         return qs.filter(**lookup_data)  # self.user_field=self.request.user

#         # * lookup_data = {'owner': self.request.user}


# class UserQueryGroupMixin:
#     # user_field = 'user'
#     allow_staff_view = False

#     def get_queryset(self, *args, **kwargs):
#         user = self.request.user

#         # lookup_data = {}
#         # lookup_data[self.user_field] = self.request.user
#         qs = super().get_queryset(*args, **kwargs)

#         users_in_group = Group.objects.get(name="StaffProductEditor").user_set.all()
#         me_group = Group.objects.get(name="PrdEditor").user_set.all()
#         if self.allow_staff_view and user.is_staff:
#             # if user.is_staff:
#             return qs
#         if user in users_in_group:
#             return qs.filter(user=user)
#         if user in me_group:
#             return qs.filter(user=user)
#         return None

#         return qs.filter(**lookup_data)  # self.user_field=self.request.user
