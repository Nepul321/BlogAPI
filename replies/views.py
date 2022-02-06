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

@api_view(['GET', 'DELETE'])
def ReplyDetailDeleteView(request, id):
    qs = Reply.objects.filter(id=id)
    if not qs:
        return Response({"detail" : "Reply not found"}, status=404)

    obj = qs.first()
    token = request.COOKIES.get("jwt")
    if request.method == "DELETE":
        if not token:
            return Response({"detail" : "Unauthenticated"}, status=403)
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({"detail" : "Unauthenticated"}, status=403)
        user = User.objects.filter(id=payload['id']).first()
        if user == obj.user or user.is_superuser:
            obj.delete()
            return Response({"detail" : "Reply deleted"}, status=200)
    serializer = ReplySerializer(obj)
    data = serializer.data
    return Response(data, status=200)