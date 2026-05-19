from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from firebase_admin import auth as firebase_auth

from .models import User
from .serializers import UserSerializer
from .authentication import FirebaseAuthentication


class UserViewSet(viewsets.ViewSet):
    authentication_classes = [FirebaseAuthentication]

    def get_permissions(self):
        if self.action == 'create':
            # Solo admins pueden crear usuarios
            return [IsAuthenticated()]
        return [IsAuthenticated()]
    
    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        # Verificar que quien crea es Admin
        if request.user.role.name != 'Administrador':
            return Response({"error":"you don't have permissions"}, status=403)
        
        data = request.data
        try:
            user = firebase_auth.create_user(
                email=data['email'],
                password="Temp1234!"
            )
            link = firebase_auth.generate_password_reset_link(data['email'])
            print("RESET LINK:", link)

            new_user = User.objects.create(
                firebase_uid=user.uid,
                name=data['name'],
                last_name=data['last_name'],
                contact_number=data['contact_number'],
                emergency_contact_number=data.get('emergency_contact_number'),
                gender=data.get('gender'),
                email=data['email'],
                role_id=data['role'],
                must_change_password=True
            )
            return Response({"message": "Usuario creado"}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

    def partial_update(self, request, pk=None):
        if request.user.role.name != 'Administrador':
            return Response({"error": "No tienes permisos"}, status=403)

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=404)

        if 'email' in request.data and request.data['email'] != user.email:
            try:
                firebase_auth.update_user(user.firebase_uid, email=request.data['email'])
            except Exception as e:
                return Response({"error": f"Firebase error: {str(e)}"}, status=400)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['get'])
    def me(self, request):
        # request.user ya es el User de Django real ✅
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def students(self, request):
        students = User.objects.filter(role__name='Student')
        serializer = UserSerializer(students, many=True)
        return Response(serializer.data)