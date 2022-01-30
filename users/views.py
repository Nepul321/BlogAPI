import uuid
from rest_framework.response import Response

from users.models import (
    UserKey,
    PasswordResetEvent
)
from .serializers import (
    UserSerializer,
    CreateUserSerializer,
    ChangePasswordSerializer,
    ResetPasswordSerializer
)
from base.models import User
import jwt
import datetime
from rest_framework.decorators import api_view
from .decorators import login_required, unauthenticated_user
from src.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from src.settings import DEBUG

if DEBUG:
    current_host = "http://localhost:8000"
else:
    current_host = ""

@api_view(['GET'])
def UserListView(request):
    qs = User.objects.filter(is_active=True)
    serializer = UserSerializer(qs, many=True)
    data = serializer.data
    return Response(data, status=200)

@api_view(['POST'])
@unauthenticated_user
def RegisterUserView(request):
    data = request.data
    serializer = CreateUserSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        qs = UserKey.objects.filter(user__email=data['email'])
        obj = qs.first()
        subject = "Verify your email"
        message = f"Thanks for signing up. \n Verify your email - {current_host}/api/users/{obj.key}/activate/"
        email_from = EMAIL_HOST_USER
        recipient_list = [obj.user.email, ]
        send_mail(subject, message, email_from, recipient_list)
        return Response({"detail" : "Account created. Verification email sent"}, status=201)

    return Response({"detail" : "Invalid data"}, status=400)

@api_view(['POST'])
@unauthenticated_user
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

    if user.is_active == False:
        return Response({"message" : "User is not active"})

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

@api_view(['GET', 'POST'])
@login_required
def LoggedInUserView(request):
    token = request.COOKIES.get('jwt')
    payload = jwt.decode(token, 'secret', algorithms=['HS256'])

    user = User.objects.filter(id=payload['id']).first()

    if request.method == "POST":
        serializer = UserSerializer(instance=user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)

    serializer = UserSerializer(user)

    return Response(serializer.data, status=200)

@api_view(['POST'])
@login_required
def LogoutView(request):
    response = Response()
    response.delete_cookie('jwt')
    response.status_code = 200
    response.data = {
        "detail" : "Logged out successfully"
    }
    return response

@api_view(['POST'])
@unauthenticated_user
def AccountVerification(request, token):
    qs = UserKey.objects.filter(key=token)
    if not qs:
        return Response({"detail" : "Verification token not found"}) 
    not_activated = qs.filter(activated=False)
    if not not_activated:
        return Response({"detail" : "Verification token already activated"})
    obj = not_activated.first()
    obj.activated = True
    obj.user.is_active = True
    obj.save()
    obj.user.save()
    return Response({"detail" : "Account activated. Login."})

@api_view(['POST'])
@login_required
def ChangePasswordView(request):
    token = request.COOKIES.get('jwt')
    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    data = request.data
    user = User.objects.filter(id=payload['id']).first()
    context = {'user' : user}
    serializer = ChangePasswordSerializer(data=data, context=context)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    payloadnew = {
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow()
    }
    newtoken = jwt.encode(payloadnew, 'secret', algorithm='HS256')

    response = Response()


    response.status_code = 200

    response.set_cookie(key="jwt", value=newtoken, httponly=True)
    response.data = {
        "jwt" : newtoken
    }

    return response
    
@api_view(['POST'])
def PasswordResetView(request):
    data = request.data
    email = data['email'] or None
    if not email or email == "":
        return Response({"detail" : "No email given"})
    qs = User.objects.filter(email=email)
    if not qs:
        return Response({"detail" : "User with the email does not exist"})

    obj = qs.first()
    event = PasswordResetEvent.objects.create(
        user=obj,
        key=uuid.uuid4()
    )
    event.save()
    subject = "Reset Your Password"
    message = f"Reset Your Password - {current_host}/api/users/password/reset/{event.key}/"
    email_from = EMAIL_HOST_USER
    recipient_list = [obj.email, ]
    send_mail(subject, message, email_from, recipient_list)
    return Response(data, status=200)

@api_view(['GET', 'POST'])
def PasswordResetFormView(request, token):
    qs = PasswordResetEvent.objects.filter(key=token)
    if not qs:
        return Response({"detail" : "Token does not exist"})

    obj = qs.first()
    if obj.activated == True:
        return Response({"detail" : "This token has already been used"})

    if request.method == "POST":
        context = {"user" : obj.user}
        data = request.data
        serializer = ResetPasswordSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        obj.activated = True
        obj.save()
        return Response({"detail" : "Successfully Password reset successful"}, status=200)

    return Response({}, status=200)