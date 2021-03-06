from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import (
    SubReply
)

from replies.models import Reply

from .serializers import (
    SubReplyActionSerializer,
    SubReplySerializer
)

import jwt

from base.models import User

from users.decorators import login_required

@api_view(["GET"])
def SubreplylistView(request):
    context = {"request" : request}
    qs = SubReply.objects.all()
    serializer = SubReplySerializer(qs, many=True, context=context)
    data = serializer.data
    return Response(data, status=200)

@api_view(['GET'])
def ReplySubRepliesView(request, id):
    context = {"request" : request}
    replyQs = Reply.objects.filter(id=id)
    if not replyQs:
        return Response({"detail" : "Comment not found"}, status=404)
    obj = replyQs.first()
    subreplyQs = SubReply.objects.filter(reply=obj)
    serializer = SubReplySerializer(subreplyQs, many=True, context=context)
    data = serializer.data
    return Response(data, status=200)

@api_view(['GET', 'DELETE'])
def SubReplyDetailDeleteView(request, id):
    context = {"request" : request}
    qs = SubReply.objects.filter(id=id)
    if not qs:
        return Response({"detail" : "Sub Reply not found"}, status=404)

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
            return Response({"detail" : "Sub Reply deleted"}, status=200)
    serializer = SubReplySerializer(obj, context=context)
    data = serializer.data
    return Response(data, status=200)

@api_view(['POST'])
@login_required
def SubReplyLikeUnlikeView(request):
    context = {"request" : request}
    serializer = SubReplyActionSerializer(data=request.data, context=context)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    id = data.get("id")
    action = data.get("action")
    qs = SubReply.objects.filter(id=id)
    if not qs:
        return Response({"detail" : "Sub Reply does not exist"}, status=404)
    obj = qs.first()
    auth = request.headers['Authorization']
    token = auth.replace("Bearer ", "")
    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    user = User.objects.filter(id=payload['id']).first()

    if action == "like":
        obj.likes.add(user)
        serializer = SubReplySerializer(obj, context=context)
        return Response(serializer.data, status=200)
    elif action == "unlike":
        obj.likes.remove(user)
        serializer = SubReplySerializer(obj, context=context)
        return Response(serializer.data, status=200)

    return Response({}, status=401)

@api_view(['POST'])
@login_required
def SubReplyCreateView(request):
    context = {"request" : request}
    data = request.data
    reply_id = data.get("reply")
    if not reply_id:
        return Response({"detail" : "Reply not given"}, status=401)
    serializer = SubReplySerializer(data=data, context=context)
    serializer.is_valid(raise_exception=True)
    replies = Reply.objects.filter(id=int(data.get("reply")))
    if not replies:
        return Response({"detail" : "Reply does not exist"}, status=404)

    reply = replies.first()
    auth = request.headers['Authorization']
    token = auth.replace("Bearer ", "")
    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    user = User.objects.filter(id=payload['id']).first()

    serializer.save(
      user=user,
      reply=reply
    )

    return Response(serializer.data, status=201)