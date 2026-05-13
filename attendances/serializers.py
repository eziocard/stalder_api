from rest_framework import serializers
from .models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_lastname = serializers.CharField(source='student.last_name', read_only=True)
    level_name = serializers.CharField(source='level.name', read_only=True)
    recorded_by_name = serializers.CharField(source='recorded_by.name', read_only=True)

    class Meta:
        model = Attendance
        fields = [
            'id',
            'student',        
            'student_name',    
            'student_lastname', 
            'level',           
            'level_name',      
            'recorded_by',      
            'recorded_by_name', 
            'date',
            'status',
            'notes',
            'created_at',
        ]
        read_only_fields = ('id', 'created_at')


class BulkAttendanceSerializer(serializers.Serializer):
    level = serializers.IntegerField()
    date = serializers.DateField()
    recorded_by = serializers.IntegerField()
    attendances = serializers.ListField(
        child=serializers.DictField()
    )

    def validate_attendances(self, value):
        valid_statuses = ['present', 'absent', 'late', 'justified']
        for item in value:
            if 'student' not in item:
                raise serializers.ValidationError('each item must has student')
            if 'status' not in item:
                raise serializers.ValidationError('each item must has status')
            if item['status'] not in valid_statuses:
                raise serializers.ValidationError(f"Status invalid: {item['status']}")
        return value
