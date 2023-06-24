from rest_framework import serializers
from myusers.models import NewUser
from rest_framework_simplejwt.tokens import RefreshToken


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """

    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = NewUser
        fields = ("email", "username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = "__all__"
        # fields = ('id', 'username', 'first_name',
        #           'email',)


class UserPublicSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    this_is_not_ideal = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    profile_pic = serializers.ImageField(read_only=True)
    bio = serializers.CharField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    # is_active = serializers.BooleanField(read_only=True)
    # date_joined = serializers.DateTimeField(read_only=True)

    # class Meta:
    #     model = NewUser
    #     field = '__all__'

    def get_name(self, obj):
        name = obj.first_name
        if name == "":
            name = obj.email
        return name


class UserProfileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    email = serializers.EmailField(read_only=True)
    profile_pic = serializers.ImageField(required=False)
    first_name = serializers.CharField(required=False)

    class Meta:
        model = NewUser
        # fields = ('first_name', 'last_name', 'email',)
        fields = (
            "id",
            "username",
            "first_name",
            "email",
            "name",
            "profile_pic",
            "isAdmin",
        )

    def get_name(self, obj):
        name = obj.first_name
        if name == "":
            name = obj.email
        return name

    def get_isAdmin(self, obj):
        return obj.is_staff

    # '''or use method below'''

    # def update(self, instance, validated_data):
    #     email = validated_data.pop('email')
    #     return super().update(instance, validated_data)


class UserSerializerWithToken(UserProfileSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = NewUser
        fields = (
            "id",
            "username",
            "first_name",
            "email",
            "name",
            "profile_pic",
            "isAdmin",
            "token",
        )

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        # return str(token)

        return {
            "token_refresh": str(token),
            "token_access": str(token.access_token),
        }
