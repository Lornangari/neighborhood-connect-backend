from .models import User, Post, AnonymousPost, HelpExchange
from rest_framework import generics, permissions, viewsets
from .serializers import RegisterSerializer, UserProfileSerializer, PostSerializer, AnonymousPostSerializer, HelpExchangeSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


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
