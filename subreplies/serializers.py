from rest_framework import serializers
from base.serializers import UserPublicSerializer
from .models import (
    SubReply
)

SUB_REPLY_VALIDATE = ['like', 'unlike']


class SubReplySerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = SubReply
        fields = ('id','user', 'content', 'date', 'likes')

    def get_likes(self, obj):
        return obj.likes.count()

class SubReplyActionSerializer(serializers.Serializer):
    id = serializers.CharField()
    action = serializers.CharField()
    def validate_action(self, value):
        value = value.lower().strip()
        if value not in SUB_REPLY_VALIDATE:
            raise serializers.ValidationError("This is not a valid action")
        return value