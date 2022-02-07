from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import (
    SubReply
)

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