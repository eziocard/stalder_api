from roles.models import Role
from rest_framework import viewsets,permissions

from roles.serializers import RoleSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RoleSerializer
