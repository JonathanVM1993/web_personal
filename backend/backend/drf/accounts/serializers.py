from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username','email', 'first_name','password','img', 'linkedin']
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        user = CustomUser(
            username = validated_data['username'],            
            email = validated_data['email'],
            first_name= validated_data['first_name'],
            img = validated_data['img'],
            linkedin = validated_data['linkedin']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user
    
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)