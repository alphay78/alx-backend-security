from django.db import models

# ✅ Task 0 + Task 2: Request logging model with geolocation
class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=200)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.ip_address} - {self.path} - {self.timestamp}"


# ✅ Task 1: Blocked IP model
class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)

    def __str__(self):
        return self.ip_address
