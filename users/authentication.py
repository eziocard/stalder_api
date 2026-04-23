from firebase_admin import auth as firebase_auth
from users.models import User

class FirebaseAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                decoded = firebase_auth.verify_id_token(token)
                firebase_uid = decoded['uid']
                user = User.objects.get(firebase_uid=firebase_uid)
                user.is_authenticated = True  # ← agrega esto
                request.user = user
            except Exception:
                request.user = None

        return self.get_response(request)