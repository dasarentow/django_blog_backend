from django.http import JsonResponse
from rest_framework.response import Response

from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework.viewsets import ModelViewSet

from myusers.serializers import UserSerializerWithToken


"""to deploy"""


def index(request):
    return render(request, "index.html")


"""to deploy"""


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["email"] = (user.email,)
        token["username"] = (user.username,)
        token["first_name"] = user.first_name
        token["admin"] = user.is_staff

        # ...
        return token

    # def validate(self, attrs):
    #     data = super().validate(attrs)

    #     # data['email'] = self.user.email,
    #     # data['username'] = self.user.username,

    #     serializer = UserSerializerWithToken(self.user).data
    #     for key, value in serializer.items():
    #         data[key] = value

    #     return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(["GET"])
def getRoutes(request):
    routes = [
        "/api/token",
        "/api/token/refresh",
        "/api/token/revoke",
    ]
    return Response(routes)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def getNotes(request):
#     user = request.user
#     notes = user.note_set.all()
#     # notes = Note.objects.all()
#     serializer = NoteSerializer(notes, many=True)
#     return Response(serializer.data)
