from rest_framework import serializers
from base.serializers import UserPublicSerializer
from .models import (
    Reply
)
REPLY_VALIDATE = ['like', 'unlike']

class ReplySerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Reply
        fields = ('id','user', 'content', 'date', 'likes')

    def get_likes(self, obj):
        return obj.likes.count()

class ReplyActionSerializer(serializers.Serializer):
    id = serializers.CharField()
    action = serializers.CharField()
    def validate_action(self, value):
        value = value.lower().strip()
        if value not in REPLY_VALIDATE:
            raise serializers.ValidationError("This is not a valid action")
        return value