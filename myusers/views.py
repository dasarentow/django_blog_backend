from .models import *
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
from rest_framework.generics import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    CustomUserSerializer,
    UserSerializer,
    UserPublicSerializer,
    UserProfileSerializer,
    UserSerializerWithToken,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model


User = get_user_model()


class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format="json"):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RetrieveUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


"""ADMIN"""


class UsersView(APIView):
    permission_classes = [IsAdminUser]
    # permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


"""Users"""


class userProfile(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = NewUser.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        # print("uuu: ", self.kwargs)
        user = self.request.user.email
        # print('user:', user)
        mine = NewUser.objects.filter(email=user)
        return NewUser.objects.filter(email=user)
        serializer = UserSerializer(mine, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(mine)


class userProfiles(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    queryset = NewUser.objects.all()
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = "username"
    #

    def get_queryset(self, *args, **kwargs):
        print("uuu: ", self.kwargs)
        user = self.request.user.username
        same = self.kwargs.get("username", None)
        print("user:", same)
        return NewUser.objects.filter(username=user)


class userProfileUpdate(generics.RetrieveUpdateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = UserProfileSerializer
    queryset = NewUser.objects.all()
    permission_classes = [IsAuthenticated]

    lookup_field = "pk"

    def get_queryset(self, *args, **kwargs):
        # print("uuu: ", self.kwargs)
        user = self.request.user.email
        same = self.kwargs.get("pk", None)
        # print("user:", same)
        return NewUser.objects.filter(email=user)

    # def perform_update(self, serializer):
    #     serializer.save()
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class updateUserProfile(APIView):
    def put(self, request, format=None):
        user = request.user
        email = request.user.email

        serializer = UserProfileSerializer(user, data=request.data, many=False)

        if serializer.is_valid():
            # denial = serializer.validated_data['email']
            # serializer.validated_data['field_name'] = prepared_data_variable

            serializer.save(email=email)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['PUT'])
# class updateUserProfile(generics.RetrieveUpdateAPIView):

#     serializer_class = UserSerializerWithToken
#     queryset = User.objects.all()
#     lookup_field = 'pk'

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def get_queryset(self):
#         queryset = self.request.user
#         # if isinstance(queryset, QuerySet):
#         #     # Ensure queryset is re-evaluated on each request.
#         #     queryset = queryset.all()
#         return queryset

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
