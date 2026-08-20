"""
Age-verification-by-call fallback.

Flow: a customer orders an age-restricted item (FoodItem.age_restricted=True).
If we can't trust their declared age (missing / under the minimum / not yet
verified), instead of silently rejecting the order we queue an automated
verification call and hold the order in 'pending_age_verification'.

Wire `place_verification_call` to a real IVR/voice API (Exotel, Twilio Voice,
Knowlarity, etc.) — this stub just creates the tracking record so the rest
of the order pipeline (status polling, admin dashboard) works end-to-end.
"""
from django.conf import settings
from .models import AgeVerificationRequest


def customer_needs_age_check(user, cart_items):
    """True if any item in the cart is age-restricted and the user isn't a verified adult."""
    has_restricted_item = any(ci.food_item.age_restricted for ci in cart_items)
    if not has_restricted_item:
        return False
    if user.is_age_verified and user.age and user.age >= settings.AGE_VERIFICATION_MIN_AGE:
        return False
    return True


def place_verification_call(order, user):
    """
    Creates the tracking row and (in production) calls out to the IVR provider's
    API using settings.CALL_VERIFICATION_PROVIDER_SID / _TOKEN / _FROM_NUMBER.
    Returns the AgeVerificationRequest so the caller can report status to the user.
    """
    request_obj = AgeVerificationRequest.objects.create(
        user=user, order=order, phone=user.phone, status='pending',
    )

    # --- TODO: integrate real provider here, e.g. ---
    # client = SomeVoiceProviderClient(settings.CALL_VERIFICATION_PROVIDER_SID,
    #                                   settings.CALL_VERIFICATION_PROVIDER_TOKEN)
    # call = client.calls.create(
    #     to=user.phone, from_=settings.CALL_VERIFICATION_FROM_NUMBER,
    #     ivr_script='age_verification_prompt',
    # )
    # request_obj.provider_call_id = call.sid
    # request_obj.status = 'calling'
    # request_obj.save(update_fields=['provider_call_id', 'status'])

    return request_obj
