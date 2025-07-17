from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, UserProfileView, PostViewSet, AnonymousPostViewSet, HelpExchangeViewSet, BusinessViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'anonymous-posts', AnonymousPostViewSet, basename='anonymouspost')
router.register(r'help-exchange', HelpExchangeViewSet, basename='helpexchange')
router.register(r'businesses', BusinessViewSet)



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('', include(router.urls)),
]




