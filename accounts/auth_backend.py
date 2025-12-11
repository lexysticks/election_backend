from django.contrib.auth.backends import BaseBackend
from .models import User

class NationalIDBackend(BaseBackend):
    """
    Authenticate using national_id and password
    """
    def authenticate(self, request, national_id=None, password=None, **kwargs):
        if not national_id or not password:
            return None
        try:
            user = User.objects.get(national_id=national_id)
        except User.DoesNotExist:
            return None
        if user.check_password(password) and user.is_active:
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
