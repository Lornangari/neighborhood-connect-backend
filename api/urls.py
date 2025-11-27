from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView,NeighborhoodViewSet, UserProfileView, AnnouncementViewSet, HelpPostViewSet, ReplyViewSet, PostViewSet, AnonymousPostViewSet, BusinessViewSet
from .views import CommentViewSet, EventViewSet, AnonymousPostViewSet, AnonymousCommentViewSet, NotificationViewSet
from .views import UserMeView 


router = routers.DefaultRouter()
router = DefaultRouter()
router.register(r'neighborhoods', NeighborhoodViewSet)
router.register(r'announcements', AnnouncementViewSet, basename='announcement')
router.register(r'help', HelpPostViewSet, basename='help')
router.register(r"businesses", BusinessViewSet, basename="business")
router.register(r'events', EventViewSet, basename='event')
router.register(r'anonymous-posts', AnonymousPostViewSet, basename='anonymous-post')
router.register("anonymous-comments", AnonymousCommentViewSet, basename="anonymous-comments")
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet)
router.register(r"notifications", NotificationViewSet, basename="notification")


# nested router for replies under help posts
help_router = routers.NestedDefaultRouter(router, r'help', lookup='post')
help_router.register(r'replies', ReplyViewSet, basename='help-replies')

urlpatterns = [
     path("anonymous-posts/<int:post_pk>/comments/", AnonymousCommentViewSet.as_view({
        "get": "list",
        "post": "create"
    }), name="anonymous-comments"),


    path('register/', RegisterView.as_view(), name='register'),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/me/', UserMeView.as_view(), name='user-me'),
    path('user/profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('', include(router.urls)),
    path('', include(help_router.urls)),
]






