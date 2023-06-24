from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


# class MyPersonalTokenPairSerializer(TokenObtainPairSerializer):

#     def validate(self, attrs):
#         data = super().validate(attrs)

#         data['email'] = self.email,
#         data['username'] = self.username,
#         data['first_name'] = self.first_name

#         return data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        data['email'] = self.user.email,
        data['username'] = self.user.username,
        data['first_name'] = self.user.first_name

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
