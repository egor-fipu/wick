from rest_framework import serializers

from users.models import User, Follow
from products.models import Notebook
from .services import get_coord


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'password', 'first_name', 'last_name', 'gender',
            'image'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        latitude, longitude = get_coord(self.context['request'])

        user = User(**validated_data)
        user.set_password(password)
        user.username = user.email
        user.latitude = latitude
        user.longitude = longitude
        user.save()
        return user


class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'gender', 'image')


class UserGetTokenSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[])

    class Meta:
        model = User
        fields = ('email', 'password')


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('follower', 'following')

    def validate(self, data):
        follower = data['follower']
        following = data['following']
        if follower == following:
            raise serializers.ValidationError({
                'following': 'Ошибка: невозможно понравится самому себе'
            })
        if Follow.objects.filter(follower=follower,
                                 following=following).exists():
            raise serializers.ValidationError({
                'following': 'Ошибка: Вы уже оценивали этого пользователя'
            })
        return data


class NotebookSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        model = Notebook
        exclude = ('created',)
