from django.conf import settings
from django.db import models


class ClientProfile(models.Model):
    """A hotel / restaurant / business partner that lists food on the platform."""
    HOTEL = 'hotel'
    RESTAURANT = 'restaurant'
    PARTNER = 'partner'
    BUSINESS_TYPE_CHOICES = (
        (HOTEL, 'Hotel'),
        (RESTAURANT, 'Restaurant'),
        (PARTNER, 'Business Partner'),
    )
    MODE_CHOICES = (
        ('online', 'Online'),
        ('offline', 'Offline'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_profile')
    business_name = models.CharField(max_length=200)
    business_type = models.CharField(max_length=20, choices=BUSINESS_TYPE_CHOICES, default=RESTAURANT)
    license_number = models.CharField(max_length=100, blank=True)
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='online')
    is_approved = models.BooleanField(default=False)  # admin approves new clients before they go live
    address = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    logo = models.ImageField(upload_to='client_logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name
