# attendance/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from users.authentication import FirebaseAuthentication
from .models import Attendance
from .serializers import AttendanceSerializer, BulkAttendanceSerializer


class AttendanceViewSet(viewsets.ViewSet):
    authentication_classes = [FirebaseAuthentication]

    def get_permissions(self):
        return [IsAuthenticated()]

    # GET /api/attendance/
    def list(self, request):
        attendances = Attendance.objects.select_related(
            'student', 'level', 'recorded_by'
        ).all()
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)

    # GET /api/attendance/by_level/?level_id=1&date=2026-05-01
    @action(detail=False, methods=['get'])
    def by_level(self, request):
        level_id = request.query_params.get('level_id')
        date = request.query_params.get('date')

        if not level_id:
            return Response({"error": "level_id es requerido"}, status=status.HTTP_400_BAD_REQUEST)

        filters = {'level_id': level_id}
        if date:
            filters['date'] = date

        attendances = Attendance.objects.select_related(
            'student', 'level', 'recorded_by'
        ).filter(**filters)

        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)

    # GET /api/attendance/by_student/?student_id=1
    @action(detail=False, methods=['get'])
    def by_student(self, request):
        student_id = request.query_params.get('student_id')

        if not student_id:
            return Response({"error": "student_id es requerido"}, status=status.HTTP_400_BAD_REQUEST)

        attendances = Attendance.objects.select_related(
            'student', 'level', 'recorded_by'
        ).filter(student_id=student_id)

        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)

    # POST /api/attendance/bulk/
    @action(detail=False, methods=['post'])
    def bulk(self, request):
        serializer = BulkAttendanceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        level_id = data['level']
        date = data['date']
        recorded_by_id = data['recorded_by']
        attendances_data = data['attendances']

        if Attendance.objects.filter(level_id=level_id, date=date).exists():
            return Response(
                {"error": f"Ya existe asistencia para este nivel en la fecha {date}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            records = [
                Attendance(
                    student_id=item['student'],
                    level_id=level_id,
                    recorded_by_id=recorded_by_id,
                    date=date,
                    status=item['status'],
                    notes=item.get('notes', ''),
                )
                for item in attendances_data
            ]
            Attendance.objects.bulk_create(records)
            return Response(
                {"message": f"{len(records)} asistencias registradas correctamente"},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # PATCH /api/attendance/bulk_update/
    @action(detail=False, methods=['patch'])
    def bulk_update(self, request):
        level_id = request.data.get('level')
        date = request.data.get('date')
        attendances_data = request.data.get('attendances', [])

        if not level_id or not date:
            return Response(
                {"error": "level y date son requeridos"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            updated = 0
            for item in attendances_data:
                student_id = item.get('student')
                new_status = item.get('status')
                notes = item.get('notes', '')

                if not student_id or not new_status:
                    continue

                rows = Attendance.objects.filter(
                    student_id=student_id,
                    level_id=level_id,
                    date=date,
                )

                if rows.exists():
                    rows.update(status=new_status, notes=notes)
                    updated += 1

            return Response(
                {"message": f"{updated} asistencias actualizadas correctamente"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)