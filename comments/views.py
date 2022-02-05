from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import (
    Comment
)
from .serializers import (
    CommentActionSerializer,
    CommentSerializer
)

import jwt

from base.models import User

from posts.models import Post

@api_view(['GET'])
def CommentListView(request):
    qs = Comment.objects.all()
    serializer = CommentSerializer(qs, many=True)
    data = serializer.data
    return Response(data, status=200)

@api_view(['GET'])
def PostCommentListView(request, id):
    postQs = Post.objects.filter(id=id)
    if not postQs:
        return Response({"detail" : "Post not found"}, status=404)
    obj = postQs.first()
    commentQs = Comment.objects.filter(post=obj)
    serializer = CommentSerializer(commentQs, many=True)
    data = serializer.data
    return Response(data, status=200)

@api_view(['GET', 'DELETE'])
def CommentDetailDeleteView(request, id):
    qs = Comment.objects.filter(id=id)
    if not qs:
        return Response({"detail" : "Comment not found"}, status=404)

    obj = qs.first()
    token = request.COOKIES.get("jwt")
    if not token:
        return Response({"detail" : "Unauthenticated"}, status=403)
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return Response({"detail" : "Unauthenticated"}, status=403)
    user = User.objects.filter(id=payload['id']).first()
    if request.method == "DELETE":
        if user == obj.user or user.is_superuser:
            obj.delete()
            return Response({"detail" : "Comment deleted"}, status=200)
    serializer = CommentSerializer(obj)
    data = serializer.data
    return Response(data, status=200)

@api_view(['POST'])
def CommentLikeUnlikeView(request):
    serializer = CommentActionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    id = data.get("id")
    action = data.get("action")
    qs = Comment.objects.filter(id=id)
    if not qs:
        return Response({"detail" : "Comment does not exist"}, status=404)
    obj = qs.first()
    token = request.COOKIES.get("jwt")
    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    user = User.objects.filter(id=payload['id']).first()

    if action == "like":
        obj.likes.add(user)
        serializer = CommentSerializer(obj)
        return Response(serializer.data, status=200)
    elif action == "unlike":
        obj.likes.remove(user)
        serializer = CommentSerializer(obj)
        return Response(serializer.data, status=200)

    return Response({}, status=401) 