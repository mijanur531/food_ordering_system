from django.conf import settings
from django.db import models


class DeliveryBoyProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='delivery_profile')
    vehicle_number = models.CharField(max_length=20, blank=True)
    id_proof_number = models.CharField(max_length=50, blank=True)
    is_available = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)  # admin verifies delivery boys before activation
    current_latitude = models.FloatField(null=True, blank=True)
    current_longitude = models.FloatField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"DeliveryBoy({self.user.username})"
