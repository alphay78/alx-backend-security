from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import SuspiciousIP
from .models import RequestLog  # Assuming you already have a model logging IP requests

SENSITIVE_PATHS = ['/admin', '/login', '/config', '/settings']

@shared_task
def detect_suspicious_ips():
    """
    Runs hourly to detect IPs with abnormal activity.
    """
    one_hour_ago = timezone.now() - timedelta(hours=1)
    recent_logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago)

    # Count requests per IP
    ip_counts = {}
    for log in recent_logs:
        ip_counts[log.ip_address] = ip_counts.get(log.ip_address, 0) + 1

        # Check for sensitive path access
        if log.path in SENSITIVE_PATHS:
            SuspiciousIP.objects.get_or_create(
                ip_address=log.ip_address,
                reason=f"Accessed sensitive path: {log.path}"
            )

    # Check for IPs exceeding rate limit
    for ip, count in ip_counts.items():
        if count > 100:
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                reason=f"Exceeded 100 requests/hour ({count} requests)"
            )

    return f"Checked {len(ip_counts)} IPs for anomalies"
