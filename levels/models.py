from django.db import models

class Level(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        related_name='levels',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class StudentLevel(models.Model):
    student = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='student_levels',
    )
    level = models.ForeignKey(
        Level,
        on_delete=models.CASCADE,
        related_name='student_levels',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'level')

    def __str__(self):
        return f'{self.student.name} - {self.level.name}'