from rest_framework import generics, status, permissions
from .permissions import IsClientUser,IsFreelancerUser
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView

from .serializers import FreelancerSignupSerializer,ClientSignupSerializer,UserSerializer


class FreelanceSignupView(generics.GenericAPIView):
    serializer_class = FreelancerSignupSerializer

    def post(self,request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({
            "user":UserSerializer(user,context=self.get_serializer_context()).data,
            "token":Token.objects.get(user=user).key,
            "message": "account created"
        })


class ClientSignupView(generics.GenericAPIView):
    serializer_class = ClientSignupSerializer

    def post(self,request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({
            "user":UserSerializer(user,context=self.get_serializer_context()).data,
            "token":Token.objects.get(user=user).key,
            "message": "account created"
        })


class CustomeAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer=self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        token, created= Token.objects.get_or_created(user=user)
        return Response({
            'token':token.key,
            'user_id':user.pk,
            'is_client':user.is_client
        })


class LogoutView(APIView):
    def post(self,request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)

class ClientOnlyView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsClientUser]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class FreelancerOnlyView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated & IsFreelancerUser]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

