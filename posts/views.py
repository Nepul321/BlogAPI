from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post
from users.decorators import login_required
from base.models import User
import jwt
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

@api_view(['POST'])
@login_required
def PostCreateView(request):
    context = {"request" : request}
    serializer = PostSerializer(data=request.data, context=context)
    token = request.COOKIES.get("jwt")
    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    user = User.objects.filter(id=payload['id']).first()
    if serializer.is_valid(raise_exception=True):
        serializer.save(author=user)
        data = serializer.data
        return Response(data, status=201)

    return Response({}, status=400)