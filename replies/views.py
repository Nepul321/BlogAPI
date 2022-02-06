from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import (
    ReplySerializer,
    ReplyActionSerializer
)
from .models import (
    Reply
)

import jwt

from comments.models import Comment

from base.models import User

@api_view(['GET'])
def ReplyListView(request):
    qs = Reply.objects.all()
    serializer = ReplySerializer(qs, many=True)
    data = serializer.data
    return Response(data, status=200)

@api_view(['GET'])
def CommentRepliesView(request, id):
    commentQs = Comment.objects.filter(id=id)
    if not commentQs:
        return Response({"detail" : "Comment not found"}, status=404)
    obj = commentQs.first()
    replyQs = Reply.objects.filter(comment=obj)
    serializer = ReplySerializer(replyQs, many=True)
    data = serializer.data
    return Response(data, status=200)
