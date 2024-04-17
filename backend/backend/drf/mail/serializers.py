from rest_framework import serializers
from .models import RecoverMail

class RecoverMailSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecoverMail
        fields = ['email', 'password']
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, data):

        email = RecoverMail(
            email = data['email'],
            password = data['password']
        )

        email.save()

        return email