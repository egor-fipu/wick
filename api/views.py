from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (serializers, viewsets, mixins, status, permissions,
                            filters)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from products.models import Notebook
from users.models import User
from .filters import NotebookFilter, UserFilter
from .serializers import (UserSerializer, UserGetTokenSerializer,
                          FollowSerializer, UsersListSerializer,
                          NotebookSerializer)
from .services import check_follow


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


class UsersViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UsersListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserFilter


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
        data = check_follow(follower, following)
        if data:
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NotebookViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Notebook.objects.all()
    serializer_class = NotebookSerializer
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    filterset_class = NotebookFilter
    ordering_fields = ('price',)
    filterset_fields = ('name',)
