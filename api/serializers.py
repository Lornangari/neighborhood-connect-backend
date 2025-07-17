from rest_framework import serializers
from .models import User, Post, AnonymousPost, HelpExchange, Business, Comment
from django.contrib.auth.password_validation import validate_password

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


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'neighborhood']
        read_only_fields = ['id', 'username', 'email']  
 

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    neighborhood = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'neighborhood', 'created_at']
        read_only_fields = ['id', 'author', 'neighborhood', 'created_at']


class AnonymousPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymousPost
        fields = ['id', 'message', 'neighborhood', 'created_at']
        read_only_fields = ['id', 'neighborhood', 'created_at']



class HelpExchangeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    neighborhood = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = HelpExchange
        fields = ['id', 'type', 'category', 'title', 'description', 'contact_info', 'user', 'neighborhood', 'created_at']
        read_only_fields = ['id', 'user', 'neighborhood', 'created_at']


class BusinessSerializer(serializers.ModelSerializer):
    total_likes = serializers.IntegerField(source='total_likes', read_only=True)

    class Meta:
        model = Business
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['user', 'created_at']
