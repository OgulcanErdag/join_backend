from rest_framework import serializers
from user_auth_app.models import UserProfile
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)  # 🔥 Username sicherstellen
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = UserProfile
        fields = ["user", "username", "email", "bio", "location"]

class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        """ Überprüft, ob Passwörter übereinstimmen und ob die E-Mail bereits existiert. """
        if 'password' not in data or 'repeated_password' not in data:
            raise serializers.ValidationError({'password': 'Password fields are required.'})

        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({'password': 'Passwords do not match'})

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'Email already exists'})

        return data

    def create(self, validated_data):
        """ Erstellt den User, speichert das Passwort sicher und gibt den User zurück. """
        validated_data.pop('repeated_password')  # Entferne das wiederholte Passwort

        user = User(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])  # Sicher speichern (hashen)
        user.save()

        return user