from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .models import User
from .serializers import UserSerializer, UserLoginSerializer, UserLogoutSerializer
from django.contrib.auth import authenticate

class Record(generics.ListCreateAPIView):
    # get method handler
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Login(generics.GenericAPIView):
    # get method handler
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    user_id = 6

    def post(self, request, *args, **kwargs):
        serializer_class = UserLoginSerializer(data=request.data)
        # serializer = UserLoginSerializer(data=request.data)

        # serializer_class.is_valid(raise_exception=True)

        # # Retrieve the validated data from the serializer
        # validated_data = serializer_class.validated_data

        # # Retrieve the username and password from the validated data
        # username = validated_data['user_id']
        # password = validated_data['password']

        # # Authenticate the user
        # user = authenticate(Username=username, password=password)

        # if user is not None:
        #     # User is authenticated, get the user ID
        #     self.user_id = user.id
        #     print("user_id " + str(self.user_id))

        print ("fff")
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class Logout(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserLogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = UserLogoutSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


def index(request):
    return redirect('/api/login')