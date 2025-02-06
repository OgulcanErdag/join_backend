from rest_framework import generics
from user_auth_app.models import UserProfile
from .serializers import UserProfileSerializer, RegistrationSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class CustomLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")  # Nutzer gibt E-Mail ein
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)  # User anhand der E-Mail suchen
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=400)

        user = authenticate(username=user.username, password=password)  # Mit Username authentifizieren

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "username": user.username, "email": user.email}, status=200)
        else:
            return Response({"error": "Invalid credentials"}, status=400)

class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'token': token.key,
                'username': saved_account.username,
                'email': saved_account.email                
            }
        else:
            data=serializer.errors
        return Response(data)     

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()  # Löscht das Token
        return Response({'message': 'Logged out successfully'})   
     
