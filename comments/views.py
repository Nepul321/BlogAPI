from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import (
    Comment
)
from .serializers import (
    CommentActionSerializer,
    CommentSerializer
)

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