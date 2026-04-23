from django.db import models

# Create your models here.
class User(models.Model):
    firebase_uid = models.CharField(max_length=128, unique=True) 
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    emergency_contact_number = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(unique=True)
    role = models.ForeignKey(
        'roles.Role',
        on_delete=models.SET_NULL,
        related_name='users',
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)  # <-- agrega esto
    must_change_password = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name