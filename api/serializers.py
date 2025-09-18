from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import (
    User, Neighborhood, Post, AnonymousPost, 
    Business, Comment, Event
)
from .models import HelpPost, Reply

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
from rest_framework import serializers
from .models import Announcement

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'



# Help-exchange serializer
# class ReplySerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source='user.username')

#     class Meta:
#         model = Reply
#         fields = ('id', 'user', 'message', 'created_at')


# class HelpPostSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source='user.username')
#     replies = ReplySerializer(many=True, read_only=True)

#     class Meta:
#         model = HelpPost
#         fields = ('id', 'user', 'type', 'title', 'description', 'created_at', 'replies')



# serializers.py

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

# class HelpPostSerializer(serializers.ModelSerializer):
#     user = serializers.CharField(source='user.username', read_only=True)
#     profile = serializers.SerializerMethodField()
#     replies = ReplySerializer(many=True, read_only=True)

#     class Meta:
#         model = HelpPost
#         fields = ['id', 'user', 'profile', 'type', 'title', 'description', 'created_at', 'replies']

#     def get_profile(self, obj):
#         profile = getattr(obj.user, 'userprofile', None)
#         if profile and profile.avatar:
#             return profile.avatar.url
#         return None

# updated help post serializer
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
class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    neighborhood = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'neighborhood', 'created_at']
        read_only_fields = ['id', 'author', 'neighborhood', 'created_at']


# Anonymous Post Serializer
class AnonymousPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymousPost
        fields = ['id', 'message', 'neighborhood', 'created_at']
        read_only_fields = ['id', 'neighborhood', 'created_at']


# Help Exchange Serializer
# class HelpExchangeSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField(read_only=True)
#     neighborhood = serializers.StringRelatedField(read_only=True)

#     class Meta:
#         model = HelpExchange
#         fields = [
#             'id', 'type', 'category', 'title', 'description', 
#             'contact_info', 'user', 'neighborhood', 'created_at'
#         ]
#         read_only_fields = ['id', 'user', 'neighborhood', 'created_at']


# Business Serializer
class BusinessSerializer(serializers.ModelSerializer):
    total_likes = serializers.IntegerField(source='total_likes', read_only=True)

    class Meta:
        model = Business
        fields = '__all__'

# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

# Event Serializer


class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.ReadOnlyField(source='organizer.username')
    neighborhood = serializers.ReadOnlyField(source='neighborhood.id')

    class Meta:
        model = Event
        fields = '__all__'
