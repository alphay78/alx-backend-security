import requests
from django.utils import timezone
from django.core.cache import cache
from django.http import HttpResponseForbidden
from .models import RequestLog, BlockedIP


class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = self.get_client_ip(request)

        # ✅ Skip tracking for localhost or internal IPs
        if ip_address in ("127.0.0.1", "::1"):
            return self.get_response(request)

        # ✅ Block requests from blacklisted IPs
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("Access denied: Your IP has been blocked.")

        path = request.path
        timestamp = timezone.now()

        # ✅ Check cache for geolocation data (24-hour cache)
        cached_data = cache.get(ip_address)
        if cached_data:
            country, city = cached_data
        else:
            country, city = self.get_geolocation(ip_address)
            cache.set(ip_address, (country, city), 60 * 60 * 24)

        # ✅ Log the request
        RequestLog.objects.create(
            ip_address=ip_address,
            path=path,
            timestamp=timestamp,
            country=country,
            city=city,
        )

        return self.get_response(request)

    def get_client_ip(self, request):
        """Extracts the client IP from headers."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")

    def get_geolocation(self, ip):
        """Fetches country and city using ipapi.co API."""
        try:
            response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5)
            data = response.json()
            country = data.get("country_name", "Unknown")
            city = data.get("city", "Unknown")
        except Exception:
            country, city = "Unknown", "Unknown"
        return country, city
