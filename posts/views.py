from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post
from users.decorators import login_required
from base.models import User
import jwt
from .serializers import PostSerializer, PostActionSerializer

@api_view(['GET'])
def PostsListView(request):
    context = {"request" : request}
    qs = Post.objects.all()
    serializer = PostSerializer(qs, many=True, context=context)
    data = serializer.data
    return Response(data, status=200)

@api_view(['GET', 'DELETE', 'POST'])
def PostDetailView(request, id):
    context = {"request" : request}
    qs = Post.objects.filter(id=id)
    if not qs:
        return Response({"detail" : "Post does not exist"}, status=404)
    obj = qs.first()
    token = request.COOKIES.get("jwt")
    if request.method == "POST":
        if not token:
            return Response({"detail" : "Unauthenticated"}, status=403)
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({"detail" : "Unauthenticated"}, status=403)
        user = User.objects.filter(id=payload['id']).first()
        serializer = PostSerializer(instance=obj, data=request.data, context=context)
        if not user:
            return Response({"detail" : "Unauthenticated"}, status=403)
        if serializer.is_valid(raise_exception=True):
            if obj.author == user:
                serializer.save()
                return Response(serializer.data, status=200)
    if request.method == "DELETE":
        if not token:
            return Response({"detail" : "Unauthenticated"}, status=403)
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({"detail" : "Unauthenticated"}, status=403)
        user = User.objects.filter(id=payload['id']).first()
        serializer = PostSerializer(instance=obj, data=request.data, context=context)
        if not user:
            return Response({"detail" : "Unauthenticated"}, status=403)
        if obj.author == user or user.is_superuser:
            obj.delete()
            return Response({"detail" : "Post deleted"}, status=200)
    
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

@api_view(['POST'])
@login_required
def PostLikeUnlikeView(request):
    context = {"request" : request}
    serializer = PostActionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    id = data.get("id")
    action = data.get("action")
    qs = Post.objects.filter(id=id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    token = request.COOKIES.get("jwt")
    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    user = User.objects.filter(id=payload['id']).first()

    if action == "like":
        obj.likes.add(user)
        serializer = PostSerializer(obj, context=context)
        return Response(serializer.data, status=200)
    elif action == "unlike":
        obj.likes.remove(user)
        serializer = PostSerializer(obj, context=context)
        return Response(serializer.data, status=200)

    return Response({}, status=401) 
