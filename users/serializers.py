from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True)
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('id', 'created_at')