from rest_framework.response import Response
from .serializers import (
    UserSerializer,
    CreateUserSerializer
)
from base.models import User
from rest_framework.decorators import api_view

@api_view(['GET'])
def UserListView(request):
    qs = User.objects.filter(is_active=True)
    serializer = UserSerializer(qs, many=True)
    data = serializer.data
    return Response(data, status=200)

@api_view(['POST'])
def RegisterUserView(request):
    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({"detail" : "Account created"}, status=201)

    return Response({"message" : "Invalid data"}, status=400)