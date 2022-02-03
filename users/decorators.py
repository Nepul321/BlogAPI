from rest_framework.response import Response
import jwt
from base.models import User

def login_required(view):
    def wrapper_function(request, *args, **kwargs):
        token = request.COOKIES.get('jwt')
        if not token:
           return Response({"detail" : "Unauthenticated"}, status=401)
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user = User.objects.filter(id=payload['id']).first()
        except jwt.ExpiredSignatureError:
            return Response({"detail" : "Unauthenticated"}, status=401)

        if not user:
            return Response({"detail" : "Unauthenticated"}, status=401)

        else:
            return view(request, *args, **kwargs)

    return wrapper_function

def unauthenticated_user(view_func):
    def wrapper_function(request, *args, **kwargs):
        token = request.COOKIES.get("jwt")
        user = None
        if token:
            return Response({"detail" : "You are logged in"})

        try:
            if token:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
                user = User.objects.filter(id=payload['id']).first()
        except jwt.ExpiredSignatureError:
               return view_func(request, *args, **kwargs)
        
        if user:
            return Response({"detail" : "You are logged in"})
        return view_func(request, *args, **kwargs)
    return wrapper_function