from rest_framework.response import Response
from .serializers import UserSerializer
from base.models import User
from rest_framework.decorators import api_view

@api_view(['GET'])
def UserListView(request):
    qs = User.objects.filter(is_active=True)
    serializer = UserSerializer(qs, many=True)
    data = serializer.data
    return Response(data, status=200)
