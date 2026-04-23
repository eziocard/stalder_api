from rest_framework import viewsets, status
from rest_framework.response import Response
from firebase_admin import auth as firebase_auth
from django.conf import settings

from .models import User
from .serializers import UserSerializer
from rest_framework.decorators import action

class UserViewSet(viewsets.ViewSet):

    def create(self, request):
        data = request.data

        try:
            # 1. Crear usuario en Firebase
            user = firebase_auth.create_user(
                email=data['email'],
                password="Temp1234!"  # contraseña temporal
            )

            # 2. Generar link para reset password
            link = firebase_auth.generate_password_reset_link(data['email'])

            # 👉 aquí deberías enviar email con ese link
            print("RESET LINK:", link)

            # 3. Guardar en Django
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

            return Response({"message": "User created"}, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=400)
    
    def partial_update(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        # Si cambia el email, actualizar también en Firebase
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

        user = request.user

        if not user:
            return Response({"error": "Unauthorized"}, status=401)

        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def students(self, request):
        students = User.objects.filter(role__name='Student')
        serializer = UserSerializer(students, many=True)
        return Response(serializer.data)
    

