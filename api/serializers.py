from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import (User, Neighborhood, Post, AnonymousPost, Business, Comment, Event,  HelpPost, Reply)

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'neighborhood']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

# User Serializer 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_staff', 'is_superuser']

# Neighborhood Serializer
class NeighborhoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neighborhood
        fields = ['id', 'name']


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    avatar = serializers.ImageField(required=False)
    # role = serializers.CharField(source='user.role')  # if you added a 'role' field
    class Meta:
        model = User
        fields = ['username', 'email', 'avatar']



#AnnouncementSerializer
from .models import Announcement

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'


from rest_framework import serializers
from .models import HelpPost, Reply, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['avatar']

class ReplySerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    profile = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        fields = ['id', 'user', 'profile', 'message', 'created_at']

    def get_profile(self, obj):
        profile = getattr(obj.user, 'userprofile', None)
        if profile and profile.avatar:
            return profile.avatar.url
        return None



# Help post-serializer
class HelpPostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    replies = ReplySerializer(many=True, read_only=True)
    reply_count = serializers.SerializerMethodField()

    class Meta:
        model = HelpPost
        fields = ('id', 'user', 'type', 'title', 'description', 'created_at', 'replies', 'reply_count')

    def get_reply_count(self, obj):
        return obj.replies.count()
    
    def get_profile(self, obj):
         profile = getattr(obj.user, 'userprofile', None)
         if profile and profile.avatar:
            return profile.avatar.url
         return None




# Post Serializer

# class CommentSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField(read_only=True)
#     post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), write_only=True)

#     class Meta:
#         model = Comment
#         fields = ['id', 'user', 'text', 'created_at', 'post']




# class PostSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField(read_only=True)
#     comments = CommentSerializer(many=True, read_only=True)

#     class Meta:
#         model = Post
#         fields = ['id', 'user', 'message', 'likes', 'created_at', 'comments']



class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), write_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'created_at', 'post']  # removed trailing comma


class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'message', 'likes', 'created_at', 'comments']  # removed trailing comma




# Business serializer
class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ["id", "name", "description", "category", "image", "contact_info", "created_at"]
        


# Event Serializer
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


# AnonymousPosts Serializer
from .models import AnonymousPost, AnonymousComment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymousComment
        fields = ["id", "text", "created_at"]

class AnonymousPostSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)
    liked_by_user = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = AnonymousPost
        fields = ["id", "text", "image", "created_at", "likes_count", "comments_count", "liked_by_user", "comments"]

    def get_liked_by_user(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False


# notification

from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "verb", "description", "url", "unread", "created_at"]
        read_only_fields = ["id", "created_at"]
