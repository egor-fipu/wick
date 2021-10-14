from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (CreateUserViewSet, APIUserGetToken, APIFollow)

router_v1 = SimpleRouter()
router_v1.register(r'clients/create', CreateUserViewSet, basename='create')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('clients/token/', APIUserGetToken.as_view()),
    path('clients/<int:following_id>/match/', APIFollow.as_view()),
]
