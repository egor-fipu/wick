from rest_framework import serializers

from users.models import User
from .utilities import watermark_photo


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email', 'password', 'first_name', 'last_name', 'gender', 'image'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')

        watermark_photo(
            validated_data['image'],
            f'users/media/users/{validated_data["email"]}.png',
            pos=(0, 0)
        )
        validated_data['image'] = f'users/{validated_data["email"]}.png'

        user = User(**validated_data)
        user.set_password(password)
        user.username = user.email
        user.save()
        return user


class UserGetTokenSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[])

    class Meta:
        model = User
        fields = ('email', 'password')
