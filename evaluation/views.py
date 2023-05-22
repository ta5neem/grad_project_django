from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from modelfolder import connection_database 
# from modelfolder import main ,PoseDetector,motion,more_functions,connection_database
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.apps import apps



class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
    


# Register API
class RegisterAPI(generics.GenericAPIView):
    
    authentication_classes = []  # Allow unauthenticated requests
    permission_classes = [AllowAny]  # Allow all users to access this view

    serializer_class = RegisterSerializer
 
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })    


class AppName:
    def get_app_name():
        myapp_config = apps.get_app_config('evluation')  # Replace 'myapp' with your app name
        return myapp_config.name


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    id_user= None

    

    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    

    @csrf_exempt
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        # Store user id in your database
        user_id = user.id
        self.id_user= user_id
        # Call function in utils.py with user_id as argument

        print("my_variable" + str(user_id))
        # main.set_user_id(user_id)
        # s= connection_database.DataBase()
        # s.set_user_id(user_id)


        return super(LoginAPI, self).post(request, format=None)