from rest_framework import serializers
from base.models import User
from .models import (
    Comment
)

COMMENT_VALIDATE = ['like', 'unlike']

class UserPublicSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, allow_blank=True, read_only=True)
    class Meta:
        model = User
        fields = [
            'username',  
            'name',
        ]

class CommentSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Comment
        fields = ('id','user', 'content', 'date', 'likes')

    def get_likes(self, obj):
        return obj.likes.count()

class CommentActionSerializer(serializers.Serializer):
    id = serializers.CharField()
    action = serializers.CharField()
    def validate_action(self, value):
        value = value.lower().strip()
        if value not in COMMENT_VALIDATE:
            raise serializers.ValidationError("This is not a valid action")
        return value