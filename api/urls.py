from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
# from .views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView,NeighborhoodViewSet, UserProfileView, AnnouncementViewSet, HelpPostViewSet, ReplyViewSet, PostViewSet, AnonymousPostViewSet, BusinessViewSet
from .views import CommentViewSet, EventViewSet
from .views import UserMeView


router = routers.DefaultRouter()
router = DefaultRouter()
router.register(r'neighborhoods', NeighborhoodViewSet)
router.register(r'announcements', AnnouncementViewSet, basename='announcement')
router.register(r'help', HelpPostViewSet, basename='help')
# router.register(r'replies', ReplyViewSet, basename='reply')

router.register(r'posts', PostViewSet, basename='post')
router.register(r'anonymous-posts', AnonymousPostViewSet, basename='anonymouspost')
# router.register(r'help-exchange', HelpExchangeViewSet, basename='helpexchange')
router.register(r'businesses', BusinessViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'events', EventViewSet)

# nested router for replies under help posts
help_router = routers.NestedDefaultRouter(router, r'help', lookup='post')
help_router.register(r'replies', ReplyViewSet, basename='help-replies')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    # path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/me/', UserMeView.as_view(), name='user-me'),
    path('user/profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('', include(router.urls)),
    path('', include(help_router.urls)),
]






