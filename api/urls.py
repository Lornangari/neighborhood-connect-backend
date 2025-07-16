from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, UserProfileView, PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('', include(router.urls)),
]
