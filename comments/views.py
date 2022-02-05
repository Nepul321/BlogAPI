from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import (
    Comment
)
from .serializers import (
    CommentActionSerializer,
    CommentSerializer
)

@api_view(['GET'])
def CommentListView(request):
    qs = Comment.objects.all()
    serializer = CommentSerializer(qs, many=True)
    data = serializer.data
    return Response(data, status=200)