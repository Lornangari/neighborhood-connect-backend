from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Post, AnonymousPost, Business, Comment, Event
from rest_framework import generics, permissions, viewsets
from .serializers import RegisterSerializer, NeighborhoodSerializer, UserProfileSerializer, PostSerializer, AnonymousPostSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import BusinessSerializer, CommentSerializer, EventSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Post, Event, Neighborhood, Comment
from .models import Neighborhood
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer  
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .serializers import UserProfileSerializer




class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.role  
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)



class NeighborhoodViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Neighborhood.objects.all()
    serializer_class = NeighborhoodSerializer


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

# PostViewset

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        post.likes += 1
        post.save()
        return Response({'likes': post.likes})


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# AnonymousPostsViewset

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import AnonymousPost, AnonymousComment
from .serializers import AnonymousPostSerializer, CommentSerializer

class AnonymousPostViewSet(viewsets.ModelViewSet):
    queryset = AnonymousPost.objects.all().order_by("-created_at")
    serializer_class = AnonymousPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=["POST"], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True
        post.save()
        return Response({"liked": liked, "likes_count": post.likes.count()}, status=status.HTTP_200_OK)

class AnonymousCommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get("post_pk")
        return AnonymousComment.objects.filter(post_id=post_id).order_by("created_at")

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_pk")
        post = AnonymousPost.objects.get(pk=post_id)
        serializer.save(post=post)


# Eventviewset
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('-date')
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]  # Only admin can modify
        return [permissions.AllowAny()]  # Everyone can view


#AnnouncementViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS
from .models import Announcement
from .serializers import AnnouncementSerializer

class IsAdminOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        # Read permissions allowed to any authenticated user
        if request.method in SAFE_METHODS:
            return True
        # Write permissions only for admin
        return request.user and request.user.is_staff

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all().order_by('-created_at')
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAdminOrReadOnly]


# helpExchange permissions
from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow only owners or admins to edit/delete.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Only the owner or admin can edit/delete
        return obj.user == request.user or request.user.role == "admin"


#helpExchange
from rest_framework import viewsets, permissions
from .models import HelpPost, Reply
from .serializers import HelpPostSerializer, ReplySerializer

class HelpPostViewSet(viewsets.ModelViewSet):
    queryset = HelpPost.objects.all().order_by('-created_at')
    serializer_class = HelpPostSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# replyviewset
class ReplyViewSet(viewsets.ModelViewSet):
    serializer_class = ReplySerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        return Reply.objects.filter(post_id=self.kwargs['post_pk']).order_by('created_at')

    def perform_create(self, serializer):
        post_id = self.kwargs['post_pk']
        serializer.save(user=self.request.user, post_id=post_id)


# Business viewset
from rest_framework import viewsets, permissions
from .models import Business
from .serializers import BusinessSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit.
    """

    def has_permission(self, request, view):
        # Read-only for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only admins can POST/PUT/DELETE
        return request.user.is_staff

class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all().order_by("-created_at")
    serializer_class = BusinessSerializer
    permission_classes = [IsAdminOrReadOnly]



from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_role_view(request):
    user = request.user
    return Response({
        'username': user.username,
        'is_superuser': user.is_superuser,
        'is_staff': user.is_staff,
        'email': user.email,
    })




@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_summary(request):
    User = get_user_model()

    data = {
        "total_users": User.objects.count(),
        "total_posts": Post.objects.count(),
        "total_events": Event.objects.count(),
        "total_neighborhoods": Neighborhood.objects.count(),
        "total_comments": Comment.objects.count(),
        
    }

    return Response(data)


