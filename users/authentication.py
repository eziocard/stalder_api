# users/authentication.py
from firebase_admin import auth as firebase_auth
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User

class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return None  # No intenta autenticar, sigue al siguiente

        token = auth_header.split('Bearer ')[1]

        try:
            # Verifica el token con Firebase
            decoded_token = firebase_auth.verify_id_token(token)
            firebase_uid = decoded_token['uid']
        except Exception:
            raise AuthenticationFailed('Token de Firebase inválido o expirado')

        try:
            # Busca el usuario en Django por su firebase_uid
            user = User.objects.get(firebase_uid=firebase_uid)
        except User.DoesNotExist:
            raise AuthenticationFailed('Usuario no encontrado en el sistema')

        if not user.is_active:
            raise AuthenticationFailed('Usuario inactivo')

        return (user, token)  # (request.user, request.auth)