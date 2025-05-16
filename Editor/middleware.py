from django.utils import timezone
from django.conf import settings
from django.contrib.auth import logout

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            now = timezone.now()

            if last_activity and (now - last_activity).total_seconds() > settings.SESSION_COOKIE_AGE:
                # Cerrar sesión si ha pasado el tiempo de inactividad
                logout(request)

            request.session['last_activity'] = now

        response = self.get_response(request)
        return response