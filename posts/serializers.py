from rest_framework import serializers
from .models import (
    Post
)
import jwt
from base.models import User
from base.serializers import UserPublicSerializer

POST_VALIDATE = ['like', 'unlike']

class PostSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    can_edit = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'content', 'date', 'likes', 'can_edit', 'is_active')

    def get_likes(self, obj):
        return obj.likes.count()

    def get_can_edit(self, obj):
        request = self.context['request']
        try:
            auth = request.headers['Authorization']
            token = auth.replace("Bearer ", "")
        except:
            token = None
        if not token:
            return False
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return False
        user = User.objects.filter(id=payload['id']).first()
        
        if not user:
            return False

        if user == obj.author or user.is_superuser:
            return True

class PostActionSerializer(serializers.Serializer):
    id = serializers.CharField()
    action = serializers.CharField()
    def validate_action(self, value):
        value = value.lower().strip()
        if value not in POST_VALIDATE:
            raise serializers.ValidationError("This is not a valid action")
        return value