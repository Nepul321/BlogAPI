from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import (
    ReplySerializer,
    ReplyActionSerializer
)
from .models import (
    Reply
)

@api_view(['GET'])
def ReplyListView(request):
    qs = Reply.objects.all()
    serializer = ReplySerializer(qs, many=True)
    data = serializer.data
    return Response(data, status=200)