from __future__ import annotations

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.utils.deprecation import MiddlewareMixin


class LoginRequiredMiddleware(MiddlewareMixin):
    """Require authentication for all views except explicitly exempt paths.

    This keeps the codebase simple: public pages are whitelisted, everything else
    redirects to LOGIN_URL with ?next=... when the user is anonymous.
    """

    def process_request(self, request):
        if getattr(request, "user", None) is not None and request.user.is_authenticated:
            return None

        path = request.path_info or "/"

        exempt_paths = set(getattr(settings, "LOGIN_REQUIRED_EXEMPT_PATHS", []))
        if path in exempt_paths:
            return None

        exempt_prefixes = tuple(getattr(settings, "LOGIN_REQUIRED_EXEMPT_PREFIXES", []))
        if exempt_prefixes and path.startswith(exempt_prefixes):
            return None

        return redirect_to_login(request.get_full_path(), settings.LOGIN_URL)
