from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, PostViewSet, CommentViewSet

router = DefaultRouter()
router.register('api/v1/users', UserViewSet)
router.register('api/v1/posts', PostViewSet)
# router.register('api/v1/posts/{pk}/comments', CommentViewSet)
