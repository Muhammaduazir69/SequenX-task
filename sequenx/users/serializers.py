from rest_framework import serializers
from .models import UserProfile
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth import get_user_model

User = get_user_model()



class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(min_length=8,write_only=True)
    password2 = serializers.CharField(min_length=8,write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number']

    def validate(self, data):
        # Check if passwords match
        password1 = data.get('password1')
        password2 = data.get('password2')
        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError("Passwords do not match")

        # Validate first name
        first_name = data.get('first_name', '')
        if len(first_name) < 2 or len(first_name) > 25 or not first_name.isalpha():
            raise serializers.ValidationError("Invalid First Name")

        # Validate last name
        last_name = data.get('last_name', '')
        if len(last_name) < 2 or len(last_name) > 25 or not last_name.isalpha():
            raise serializers.ValidationError("Invalid Last Name")

        # Validate email
        email = data.get('email', '')
        if not '@' in email or not '.' in email:
            raise serializers.ValidationError("Invalid Email")

        # Validate password
        if password1:
            if len(password1) < 8 or not any(char.isupper() for char in password1) or not any(char.islower() for char in password1) or not any(char.isdigit() for char in password1):
                raise serializers.ValidationError("Invalid Password")

        # Validate phone number
        phone_number = data.get('phone_number', '')
        if len(phone_number) < 10 or len(phone_number) > 15 or not phone_number.isdigit():
            raise serializers.ValidationError("Invalid Phone Number")

        # Validate profile picture format
        profile_picture = self.context['request'].FILES.get('profile_picture')
        if profile_picture:
            if not profile_picture.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise serializers.ValidationError("Invalid Profile Picture Format")

        return data

    def create(self, validated_data):
        # Remove password2 from validated data
        password1 = validated_data.pop('password1')
        validated_data.pop('password2', None)
        # Extract email from validated data
        email = validated_data.pop('email')
        # Create and return a new user instance
        return User.objects.create_user(email=email, password=password1, **validated_data)

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6,write_only=True)
    email = serializers.EmailField()
    tokens = serializers.SerializerMethodField()
    def get_tokens(self, obj):
        user = UserProfile.objects.get(email=obj['email'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }
    class Meta:
        model = UserProfile
        fields = ['password','email','tokens']
    def validate(self, attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')
        user = auth.authenticate(email=email,password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        return {
            'email': user.email,
            'tokens': user.tokens
        }

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'phone_number', 'profile_picture']

class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField()
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')