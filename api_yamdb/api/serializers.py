from rest_framework import serializers

from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username']

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('username не может быть me')
        return value
