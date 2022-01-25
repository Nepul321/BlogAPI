from rest_framework.response import Response
import jwt
from base.models import User

def login_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        token = request.COOKIES.get('jwt')
        if not token:
           return Response({"message" : "Unauthenticated"}, status=401)
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({"message" : "Unauthenticated"}, status=401)

        user = User.objects.filter(id=payload['id']).first()

        if not user:
            return Response({"message" : "Unauthenticated"}, status=401)

        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        token = request.COOKIES.get("jwt")
        user = None
        if token:
            return Response({"message" : "You are logged in"})

        try:
            if token:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
                user = User.objects.filter(id=payload['id']).first()
        except jwt.ExpiredSignatureError:
            pass
        
        if user:
            return Response({"message" : "You are logged in"})
        return view_func(request, *args, **kwargs)
    return wrapper_func  