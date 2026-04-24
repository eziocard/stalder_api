# users/models.py
from django.db import models

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
    is_active = models.BooleanField(default=True)
    must_change_password = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ← Esto es lo que DRF necesita
    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __str__(self):
        return self.name