from django.http import request
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import authenticate

from auth_user.models import AuthUser
from .serializers import RegistrationSerializer, ProfileSerializer

@authentication_classes([])
@permission_classes([])
@api_view(['POST'])
def register(request):

    serializer = RegistrationSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        
        return Response({
            'email':user.email,
            'username':user.username, 
            'token':Token.objects.get(user=user).key
        })
        
    return Response(serializer.errors)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    try:
        user = request.user
    except AuthUser.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)
    
    serializer = ProfileSerializer(user)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def profileUpdate(request):
    try:
        user = request.user
    except AuthUser.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)
    
    serializer = ProfileSerializer(user, data=request.data)

    if serializer.is_valid():
        serializer.save()
        
        return Response({'message':'Profile updated'})
    
    return Response({'message':'Failed'}, HTTP_400_BAD_REQUEST)


# Custom Login
class ObtainAuthTokenView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)

        if user:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            context = {
                'message':'Login Success',
                'id':user.id,
                'email':user.email,
                'token':token.key
            }
            return Response(context)
        else:
            context = {
                'message':'Invalid credentials',
            }
        
        return Response(context, status=HTTP_404_NOT_FOUND)