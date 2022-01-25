from rest_framework.response import Response
from .serializers import (
    UserSerializer,
    CreateUserSerializer
)
from base.models import User
import jwt
import datetime
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

    return Response({"detail" : "Invalid data"}, status=400)

@api_view(['POST'])
def LoginView(request):
    data = request.data
    email = data['email']
    password = data['password']

    if not email:
        return Response({"message" : "Email not entered"}, status=204)

    if not password:
        return Response({"message" : "Password not given"}, status=204)

    qs = User.objects.filter(email=email)
    if not qs:
        return Response({"message" : "User not found"}, status=404)

    user = qs.first()

    if not user.check_password(password):
        return Response({"message" : "Wrong password"}, status=401)

    payload = {
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, 'secret', algorithm='HS256')

    response = Response()

    response.status_code = 200

    response.set_cookie(key="jwt", value=token, httponly=True)
    response.data = {
        "jwt" : token
    }

    return response

@api_view(['GET'])
def LoggedInUserView(request):
    token = request.COOKIES.get('jwt')
    payload = jwt.decode(token, 'secret', algorithms=['HS256'])

    user = User.objects.filter(id=payload['id']).first()

    serializer = UserSerializer(user)

    return Response(serializer.data, status=200)

@api_view(['POST'])
def LogoutView(request):
    response = Response()
    response.delete_cookie('jwt')
    response.status_code = 200
    response.data = {
        "detail" : "Logged out successfully"
    }
    return response