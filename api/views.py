from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Post, AnonymousPost, HelpExchange, Business, Comment, Event
from rest_framework import generics, permissions, viewsets
from .serializers import RegisterSerializer, NeighborhoodSerializer, UserProfileSerializer, PostSerializer, AnonymousPostSerializer, HelpExchangeSerializer
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



class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        # Show only posts from the user's neighborhood
        user = self.request.user
        return Post.objects.filter(neighborhood=user.neighborhood).order_by('-created_at')

    def perform_create(self, serializer):
        # Automatically assign the post to the logged-in user and their neighborhood
        serializer.save(author=self.request.user, neighborhood=self.request.user.neighborhood)


class AnonymousPostViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AnonymousPostSerializer

    def get_queryset(self):
        return AnonymousPost.objects.filter(
            neighborhood=self.request.user.neighborhood
        ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            neighborhood=self.request.user.neighborhood
        )


class HelpExchangeViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = HelpExchangeSerializer
    queryset = HelpExchange.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['type', 'category']
    ordering = ['-created_at']

    def get_queryset(self):
        return HelpExchange.objects.filter(neighborhood=self.request.user.neighborhood)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, neighborhood=self.request.user.neighborhood)


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = Business.objects.all()
        neighborhood = self.request.query_params.get('neighborhood')
        business_type = self.request.query_params.get('type')
        name = self.request.query_params.get('name')
        
        if neighborhood:
            queryset = queryset.filter(neighborhood__id=neighborhood)
        if business_type:
            queryset = queryset.filter(business_type__icontains=business_type)
        if name:
            queryset = queryset.filter(name__icontains=name)
        
        return queryset


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        business = self.get_object()
        business.liked_by.add(request.user)
        return Response({'status': 'business liked'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        business = self.get_object()
        business.liked_by.remove(request.user)
        return Response({'status': 'business unliked'})

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def saved(self, request):
        saved = Business.objects.filter(liked_by=request.user)
        serializer = self.get_serializer(saved, many=True)
        return Response(serializer.data)
    
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

from .permissions import IsAdminUserOrReadOnly

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsAdminUserOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(
            organizer=self.request.user,
            neighborhood=self.request.user.neighborhood  # assuming user has neighborhood FK
        )

#AnnouncementViewSet

from rest_framework import viewsets
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


# views.py
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_user_info(request):
#     return Response({
#         'username': request.user.username,
#         'role': request.user.profile.role  # or wherever your role is stored
#     })





# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def user_info(request):
#     return Response({
#         "username": request.user.username,
#         "is_staff": request.user.is_staff,
#         "email": request.user.email,
        
#     })



# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_user_role(request):
#     user = request.user
#     return Response({
#         "username": user.username,
#         "is_admin": user.is_superuser,  
#     })


# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def user_role_view(request):
#     user = request.user
#     return Response({
#         "username": user.username,
#         "is_admin": user.is_superuser
#     })










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
