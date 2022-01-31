from rest_framework import serializers
from .models import (
    Post
)
from base.models import User

class UserPublicSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, allow_blank=True, read_only=True)
    class Meta:
        model = User
        fields = [
            'username',  
            'name',
        ]

class PostSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Post
        fields = ('title', 'author', 'content', 'date', 'likes')

    def get_likes(self, obj):
        return obj.likes.count()