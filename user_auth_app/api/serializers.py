from rest_framework import serializers
from user_auth_app.models import UserProfile
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)  # 🔥 Username hinzufügen
    email = serializers.EmailField(source='user.email', read_only=True)  # 🔥 Email hinzufügen

    class Meta:
        model = UserProfile  # Falls dein Modell anders heißt, anpassen!
        fields = ['user', 'username', 'email', 'bio', 'location']  # 🔥 `username` & `email` einfügen

class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def save(self, **kwargs):
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']

        if pw != repeated_pw:
            raise serializers.ValidationError({'error': 'Passwords do not match'})

        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username']
        )
        user.set_password(pw)
        user.save()
        return user