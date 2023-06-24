from rest_framework import permissions


class IsStaffEditorPermission(permissions.DjangoModelPermissions):
    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": [],
        "HEAD": ["%(app_label)s.view_%(model_name)s"],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }

    # you can ommit the one below unless you want to set extra permissions
    # and u are cool

    # def has_permission(self, request, view):
    #     # print('eeee', request.user.email)

    #     if not request.user.email == 'danny@email.com':
    #         return False

    #     if not request.user.is_staff:

    #         return False

    #     return super().has_permission(request, view)

    # print('view', view)
    # user = request.user

    # print('get permissions', user.get_all_permissions())
    # if user.is_staff:
    #     if user.has_perm("products.add_product"):
    #         return True
    #     if user.has_perm("products.delete_product"):
    #         return True
    #     if user.has_perm("products.view_product"):
    #         return True
    #     if user.has_perm("products.change_product"):
    #         return True

    #     return False

    # return False

    # def has_object_permission(self, request, view, obj):
    #     return obj.owner == request.user


# class IsStaffEditorPermission(permissions.DjangoModelPermissions):

#     def has_permission(self, request, view):
#         print('view', view)
#         user = request.user

#         print('get permissions', user.get_all_permissions())
#         if user.is_staff:
#             if user.has_perm("products.add_product"):
#                 return True
#             if user.has_perm("products.delete_product"):
#                 return True
#             if user.has_perm("products.view_product"):
#                 return True
#             if user.has_perm("products.change_product"):
#                 return True

#             return False

#         return False

#     # def has_object_permission(self, request, view, obj):
#     #     return obj.owner == request.user


class IsSuperUserPermission(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        user = request.user

        if user.is_superuser:
            if user.has_perm("products.view_product"):
                return True
            if user.has_perm("products.delete_product"):
                return True

            # return False

        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user
