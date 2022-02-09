from rest_framework import serializers
from base.serializers import UserPublicSerializer
from .models import (
    Comment
)

COMMENT_VALIDATE = ['like', 'unlike']

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