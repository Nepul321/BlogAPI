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

@api_view(["GET"])
def SubreplylistView(request):
    qs = SubReply.objects.all()
    serializer = SubReplySerializer(qs, many=True)
    data = serializer.data
    return Response(data, status=200)

@api_view(['GET'])
def ReplySubRepliesView(request, id):
    replyQs = Reply.objects.filter(id=id)
    if not replyQs:
        return Response({"detail" : "Comment not found"}, status=404)
    obj = replyQs.first()
    subreplyQs = SubReply.objects.filter(reply=obj)
    serializer = SubReplySerializer(subreplyQs, many=True)
    data = serializer.data
    return Response(data, status=200)

@api_view(['GET', 'DELETE'])
def SubReplyDetailDeleteView(request, id):
    qs = SubReply.objects.filter(id=id)
    if not qs:
        return Response({"detail" : "Sub Reply not found"}, status=404)

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
            return Response({"detail" : "Sub Reply deleted"}, status=200)
    serializer = SubReplySerializer(obj)
    data = serializer.data
    return Response(data, status=200)