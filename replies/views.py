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

from users.decorators import login_required

@api_view(['GET'])
def ReplyListView(request):
    context = {"request" : request}
    qs = Reply.objects.all()
    serializer = ReplySerializer(qs, many=True, context=context)
    data = serializer.data
    return Response(data, status=200)

@api_view(['GET'])
def CommentRepliesView(request, id):
    context = {"request" : request}
    commentQs = Comment.objects.filter(id=id)
    if not commentQs:
        return Response({"detail" : "Comment not found"}, status=404)
    obj = commentQs.first()
    replyQs = Reply.objects.filter(comment=obj)
    serializer = ReplySerializer(replyQs, many=True, context=context)
    data = serializer.data
    return Response(data, status=200)

@api_view(['GET', 'DELETE'])
def ReplyDetailDeleteView(request, id):
    context = {"request" : request}
    qs = Reply.objects.filter(id=id)
    if not qs:
        return Response({"detail" : "Reply not found"}, status=404)

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
            return Response({"detail" : "Reply deleted"}, status=200)
    serializer = ReplySerializer(obj, context=context)
    data = serializer.data
    return Response(data, status=200)

@api_view(['POST'])
@login_required
def ReplyLikeUnlikeView(request):
    context = {"request" : request}
    serializer = ReplyActionSerializer(data=request.data, context=context)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    id = data.get("id")
    action = data.get("action")
    qs = Reply.objects.filter(id=id)
    if not qs:
        return Response({"detail" : "Reply does not exist"}, status=404)
    obj = qs.first()
    auth = request.headers['Authorization']
    token = auth.replace("Bearer ", "")
    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    user = User.objects.filter(id=payload['id']).first()

    if action == "like":
        obj.likes.add(user)
        serializer = ReplySerializer(obj, context=context)
        return Response(serializer.data, status=200)
    elif action == "unlike":
        obj.likes.remove(user)
        serializer = ReplySerializer(obj, context=context)
        return Response(serializer.data, status=200)

    return Response({}, status=401)

@api_view(['POST'])
@login_required
def ReplyCreateView(request):
    context = {"request" : request}
    data = request.data
    comment_id = data.get("comment")
    if not comment_id:
        return Response({"detail" : "Comment not given"}, status=401)
    serializer = ReplySerializer(data=data, context=context)
    serializer.is_valid(raise_exception=True)
    comments = Comment.objects.filter(id=int(data.get("comment")))
    if not comments:
        return Response({"detail" : "Comment does not exist"}, status=404)

    comment = comments.first()
    auth = request.headers['Authorization']
    token = auth.replace("Bearer ", "")
    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    user = User.objects.filter(id=payload['id']).first()

    serializer.save(
      user=user,
      comment=comment
    )

    return Response(serializer.data, status=201)