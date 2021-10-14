from django.shortcuts import get_object_or_404
from rest_framework import serializers, viewsets, mixins, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User, Follow
from .serializers import (UserSerializer, UserGetTokenSerializer,
                          FollowSerializer)
from .utilities import send_like_email


class CreateUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class APIUserGetToken(APIView):

    def post(self, request):
        serializer = UserGetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, email=serializer.validated_data['email']
        )
        if user.check_password(serializer.validated_data['password']):
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)
            data = {
                'token': token
            }
            return Response(data=data, status=status.HTTP_200_OK)
        raise serializers.ValidationError({'password': 'Неверный пароль'})


class APIFollow(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, following_id):
        follower = request.user
        following = get_object_or_404(User, id=following_id)
        data = {
            'follower': follower.id,
            'following': following.id,
        }
        serializer = FollowSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if Follow.objects.filter(follower=following,
                                 following=follower).exists():
            send_like_email(follower=follower, following=following)
            send_like_email(follower=following, following=follower)
            data = {
                'message': f'Вы тоже понравились {following.first_name}, '
                           f'Почта участника: {following.email}'
            }
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)
