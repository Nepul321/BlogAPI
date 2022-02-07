from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(["GET"])
def SubreplylistView(request):
    return Response({}, status=200)