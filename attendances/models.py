from django.db import models

# Create your models here.
class Attendance(models.Model):

    STATUS_CHOICES = [
        ('present', 'Presente'),
        ('absent', 'Ausente'),
        ('late', 'Atrasado'),
        ('justified', 'Justificado'),
    ]

    student = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='attendances',
    )
    level = models.ForeignKey(
        'levels.Level',
        on_delete=models.CASCADE,
        related_name='attendances',
    )
    recorded_by = models.ForeignKey( 
        'users.User',
        on_delete=models.SET_NULL,
        related_name='recorded_attendances',
        null=True,
    )
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='absent')
    notes = models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'level', 'date')  

    def __str__(self):
        return f'{self.student.name} - {self.level.name} - {self.date} - {self.status}'