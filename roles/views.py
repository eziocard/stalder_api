from roles.models import Role
from rest_framework import viewsets,permissions

from roles.serializers import RoleSerializer
from users.authentication import FirebaseAuthentication

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RoleSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from firebase_admin import auth as firebase_auth

from .models import Role
from .serializers import RoleSerializer



class RoleViewSet(viewsets.ViewSet):
    authentication_classes = [FirebaseAuthentication]
    def get_permissions(self):
        if self.action == 'create':
            # Solo admins pueden crear usuarios
            return [IsAuthenticated()]
        return [IsAuthenticated()]
    
    def list(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)
    