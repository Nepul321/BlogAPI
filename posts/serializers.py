from rest_framework import serializers
from .models import (
    Post
)
import jwt
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
    can_edit = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'content', 'date', 'likes', 'can_edit')

    def get_likes(self, obj):
        return obj.likes.count()

    def get_can_edit(self, obj):
        request = self.context['request']
        token = request.COOKIES.get("jwt")
        if not token:
            return False
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return False
        user = User.objects.filter(id=payload['id']).first()
        
        if not user:
            return False

        if user == obj.author:
            return True