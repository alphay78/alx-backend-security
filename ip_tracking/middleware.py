from django.http import HttpResponseForbidden
from .models import RequestLog, BlockedIP
from datetime import datetime

class IPTrackingAndBlacklistMiddleware:
    """
    Middleware to block blacklisted IPs and log every allowed request.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)
        path = request.path

        # 🔒 Block blacklisted IPs
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP has been blocked.")

        # 🧾 Log allowed requests
        RequestLog.objects.create(ip_address=ip, path=path, timestamp=datetime.now())

        # Continue the request
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Extract client IP from request headers."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
