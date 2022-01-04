from rest_framework import serializers
from auth_user.models import AuthUser 

class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    
    class Meta:
        model = AuthUser
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def save(self):
        user = AuthUser(
            email= self.validated_data['email'],
            username = self.validated_data['username'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'Password must match!'})

        user.set_password(password)
        user.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = ['id', 'email', 'username']