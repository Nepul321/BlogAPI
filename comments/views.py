from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import (
    Comment
)

@api_view(['GET'])
def CommentListView(request):
    qs = Comment.objects.all()
    return Response({}, status=200)