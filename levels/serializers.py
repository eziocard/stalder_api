from rest_framework import serializers
from .models import Level, StudentLevel  # ← agrega StudentLevel


class LevelSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.name', read_only=True)
    teacher_lastname = serializers.CharField(source='teacher.last_name', read_only=True)

    class Meta:
        model = Level
        fields = [
            'id',
            'name',
            'teacher',
            'teacher_name',
            'teacher_lastname',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ('id', 'created_at', 'updated_at')


class StudentLevelSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_lastname = serializers.CharField(source='student.last_name', read_only=True)
    student_email = serializers.CharField(source='student.email', read_only=True)

    class Meta:
        model = StudentLevel
        fields = [
            'id',
            'student',
            'student_name',
            'student_lastname',
            'student_email',
            'level',
            'created_at',
        ]
        read_only_fields = ('id', 'created_at')