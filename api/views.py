from .models import User, Post, AnonymousPost, HelpExchange, Business, Comment
from rest_framework import generics, permissions, viewsets
from .serializers import RegisterSerializer, UserProfileSerializer, PostSerializer, AnonymousPostSerializer, HelpExchangeSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import BusinessSerializer, CommentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status





class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)