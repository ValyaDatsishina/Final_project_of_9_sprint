from django.urls import path, include
from rest_framework.authtoken import views

from .router import router
from .views import CommentViewSet

urlpatterns = [
    path('api/v1/api-token-auth/', views.obtain_auth_token),
    path('api/v1/posts/<int:pk>/comments/<int:pk_comment>/', CommentViewSet.as_view(
        {'get': 'list',
         'put': 'partial_update',
         'patch': 'partial_update',
         'delete': 'destroy'})),
    path('api/v1/posts/<int:pk>/comments/', CommentViewSet.as_view(
        {'get': 'list',
         'post': 'create'})),
    path('', include(router.urls)),
]
