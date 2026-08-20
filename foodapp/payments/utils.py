import razorpay
from django.conf import settings


def get_razorpay_client():
    return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def create_razorpay_order(order):
    """
    Creates a Razorpay order for the given Order instance. Razorpay's checkout.js
    widget on the frontend also natively supports UPI (Google Pay / PhonePe / BHIM)
    as a payment method alongside cards/netbanking — no separate integration needed.
    """
    client = get_razorpay_client()
    amount_paise = int(order.total_amount * 100)  # Razorpay expects the smallest currency unit
    razorpay_order = client.order.create({
        'amount': amount_paise,
        'currency': 'INR',
        'receipt': f'order_rcpt_{order.id}',
        'payment_capture': 1,
        'notes': {'order_id': str(order.id), 'user': order.user.username},
    })
    order.razorpay_order_id = razorpay_order['id']
    order.save(update_fields=['razorpay_order_id'])
    return razorpay_order


def verify_razorpay_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature):
    client = get_razorpay_client()
    params = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_signature': razorpay_signature,
    }
    try:
        client.utility.verify_payment_signature(params)
        return True
    except razorpay.errors.SignatureVerificationError:
        return False
