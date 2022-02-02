from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer

@api_view(['GET'])
def PostsListView(request):
    context = {"request" : request}
    qs = Post.objects.all()
    serializer = PostSerializer(qs, many=True, context=context)
    data = serializer.data
    return Response(data, status=200)

@api_view(['GET'])
def PostDetailView(request, id):
    context = {"request" : request}
    qs = Post.objects.filter(id=id)
    if not qs:
        return Response({"detail" : "Post does not exist"}, status=404)
    obj = qs.first()
    serializer = PostSerializer(obj, context=context)
    data = serializer.data
    return Response(data, status=200)