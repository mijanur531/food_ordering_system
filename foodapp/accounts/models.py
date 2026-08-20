from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Single auth table for all three app "sides" (customer / client / delivery boy)
    plus admin. user_type drives which register/login flow was used and which
    redirect happens after auth on the frontend.
    """
    CUSTOMER = 'customer'
    CLIENT = 'client'
    DELIVERY = 'delivery'
    ADMIN = 'admin'

    USER_TYPE_CHOICES = (
        (CUSTOMER, 'Customer'),
        (CLIENT, 'Client (Hotel / Business Partner)'),
        (DELIVERY, 'Delivery Boy'),
        (ADMIN, 'Admin'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default=CUSTOMER)
    phone = models.CharField(max_length=15, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    is_age_verified = models.BooleanField(default=False)
    address = models.TextField(blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class AgeVerificationRequest(models.Model):
    """
    Fallback flow: if a customer's declared age can't be trusted for an
    age-restricted item (missing, unverified, or borderline), we queue a
    call-based verification instead of blocking the order outright.
    Wire status updates to your IVR/voice provider webhook (Exotel/Twilio Voice etc).
    """
    STATUS_CHOICES = (
        ('pending', 'Pending Call'),
        ('calling', 'Call In Progress'),
        ('verified', 'Verified'),
        ('failed', 'Failed / Rejected'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='age_verification_requests')
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='age_verification_requests')
    phone = models.CharField(max_length=15)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    provider_call_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"AgeCheck #{self.id} for Order #{self.order_id} ({self.status})"
