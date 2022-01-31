from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer

@api_view(['GET'])
def PostsListView(request):
    qs = Post.objects.all()
    serializer = PostSerializer(qs, many=True)
    data = serializer.data
    return Response(data, status=200)