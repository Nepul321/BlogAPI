from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import (
    Comment
)
from .serializers import (
    CommentActionSerializer,
    CommentSerializer
)

from users.decorators import login_required

import jwt

from base.models import User

from posts.models import Post

@api_view(['GET'])
def CommentListView(request):
    context = {"request" : request}
    qs = Comment.objects.all()
    serializer = CommentSerializer(qs, many=True, context=context)
    data = serializer.data
    return Response(data, status=200)

@api_view(['GET'])
def PostCommentListView(request, id):
    context = {"request" : request}
    postQs = Post.objects.filter(id=id)
    if not postQs:
        return Response({"detail" : "Post not found"}, status=404)
    obj = postQs.first()
    commentQs = Comment.objects.filter(post=obj)
    serializer = CommentSerializer(commentQs, many=True, context=context)
    data = serializer.data
    return Response(data, status=200)

@api_view(['GET', 'DELETE'])
def CommentDetailDeleteView(request, id):
    context = {"request" : request}
    qs = Comment.objects.filter(id=id)
    if not qs:
        return Response({"detail" : "Comment not found"}, status=404)

    obj = qs.first()
    try:
        auth = request.headers['Authorization']
        token = auth.replace("Bearer ", "")
    except:
        token = None
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
            return Response({"detail" : "Comment deleted"}, status=200)
    serializer = CommentSerializer(obj, context=context)
    data = serializer.data
    return Response(data, status=200)

@api_view(['POST'])
@login_required
def CommentLikeUnlikeView(request):
    context = {"request" : request}    
    serializer = CommentActionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    id = data.get("id")
    action = data.get("action")
    qs = Comment.objects.filter(id=id)
    if not qs:
        return Response({"detail" : "Comment does not exist"}, status=404)
    obj = qs.first()
    auth = request.headers['Authorization']
    token = auth.replace("Bearer ", "")
    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    user = User.objects.filter(id=payload['id']).first()

    if action == "like":
        obj.likes.add(user)
        serializer = CommentSerializer(obj, context=context)
        return Response(serializer.data, status=200)
    elif action == "unlike":
        obj.likes.remove(user)
        serializer = CommentSerializer(obj, context=context)
        return Response(serializer.data, status=200)

    return Response({}, status=401)

@api_view(['POST'])
@login_required
def CommentCreateView(request):
    context = {"request" : request}
    data = request.data
    post_id = data.get("post")
    if not post_id:
        return Response({"detail" : "Post not given"}, status=401)
    serializer = CommentSerializer(data=data, context=context)
    serializer.is_valid(raise_exception=True)
    posts = Post.objects.filter(id=int(data.get("post")))
    if not posts:
        return Response({"detail" : "Post does not exist"}, status=404)

    post = posts.first()
    auth = request.headers['Authorization']
    token = auth.replace("Bearer ", "")
    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    user = User.objects.filter(id=payload['id']).first()

    serializer.save(
      user=user,
      post=post
    )

    return Response(serializer.data, status=201)
