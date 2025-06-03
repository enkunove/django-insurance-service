from django.utils import timezone

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated and hasattr(user, 'userprofile'):
            timezone.activate(user.userprofile.time_zone)
        else:
            timezone.deactivate()

        return self.get_response(request)
