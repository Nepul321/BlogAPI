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