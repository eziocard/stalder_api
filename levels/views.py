from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from users.authentication import FirebaseAuthentication
from .models import Level, StudentLevel
from .serializers import LevelSerializer, StudentLevelSerializer


class LevelViewSet(viewsets.ViewSet):
    authentication_classes = [FirebaseAuthentication]

    def get_permissions(self):
        return [IsAuthenticated()]

    # GET /api/levels/
    def list(self, request):
        levels = Level.objects.select_related('teacher').all()
        serializer = LevelSerializer(levels, many=True)
        return Response(serializer.data)

    # POST /api/levels/
    def create(self, request):
        if request.user.role is None or request.user.role.name != 'Admin':
            return Response({"error": "No tienes permisos"}, status=status.HTTP_403_FORBIDDEN)
        try:
            level = Level.objects.create(
                name=request.data['name'],
                teacher_id=request.data.get('teacher'),
            )
            return Response(LevelSerializer(level).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("ERROR:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # DELETE /api/levels/{id}/
    def destroy(self, request, pk=None):
        if request.user.role is None or request.user.role.name != 'Admin':
            return Response({"error": "No tienes permisos"}, status=status.HTTP_403_FORBIDDEN)
        try:
            Level.objects.get(pk=pk).delete()
        except Level.DoesNotExist:
            return Response({"error": "Level no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # GET /api/levels/{id}/students/
    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        relations = StudentLevel.objects.filter(level_id=pk).select_related('student')
        serializer = StudentLevelSerializer(relations, many=True)
        return Response(serializer.data)

    # POST /api/levels/{id}/add_student/
    @action(detail=True, methods=['post'])
    def add_student(self, request, pk=None):
        if request.user.role is None or request.user.role.name != 'Admin':
            return Response({"error": "No tienes permisos"}, status=status.HTTP_403_FORBIDDEN)
        try:
            relation, created = StudentLevel.objects.get_or_create(
                student_id=request.data['student'],
                level_id=pk,
            )
            if not created:
                return Response({"error": "El alumno ya está en este nivel"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(StudentLevelSerializer(relation).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # DELETE /api/levels/{id}/remove_student/
    @action(detail=True, methods=['delete'])
    def remove_student(self, request, pk=None):
        if request.user.role is None or request.user.role.name != 'Admin':
            return Response({"error": "No tienes permisos"}, status=status.HTTP_403_FORBIDDEN)
        try:
            StudentLevel.objects.get(
                level_id=pk,
                student_id=request.data['student']
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except StudentLevel.DoesNotExist:
            return Response({"error": "Relación no encontrada"}, status=status.HTTP_404_NOT_FOUND)