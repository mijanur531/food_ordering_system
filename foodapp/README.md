# Online Food Ordering Platform — Backend (Django + DRF)

This is the backend of the full-stack build: Django project + REST API,
covering auth for three separate user types, the veg/non-veg/international
menu system with Indian regional sub-categories, cart, checkout, age
verification, Razorpay/UPI payments, and email confirmations.

**Status: backend is complete and tested.** The HTML/Bootstrap/JS/three.js
frontend (templates + static/js) has not been added to this drop yet —
see "What's next" below.

## Project layout

```
foodapp/
├── accounts/       # Custom User model, 3 register/login flows, age-verification-by-call
├── restaurants/    # ClientProfile (hotel / restaurant / business partner)
├── menu/           # FoodCategory (veg/non_veg/international), FoodSubCategory (regional), FoodItem
├── orders/         # Cart, CartItem, Wishlist, Order, OrderItem, checkout logic
├── delivery/       # DeliveryBoyProfile, live location endpoint
├── payments/       # Razorpay order creation + signature verification
├── core/           # Contact form, admin live-monitoring feed, email helpers
├── foodapp/        # settings.py, urls.py
├── manage.py
└── requirements.txt
```

## Setup

```bash
cd foodapp
python -m venv venv
source venv/bin/activate          # venv\Scripts\activate on Windows
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_menu        # loads veg/non-veg/international + regional sub-categories
python manage.py createsuperuser  # for /admin/

python manage.py runserver
```

Then set real values (via environment variables — see `foodapp/settings.py`
for every key read) for:
- `RAZORPAY_KEY_ID` / `RAZORPAY_KEY_SECRET` — from your Razorpay dashboard
- `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD` (or swap `EMAIL_BACKEND` to your provider) for real emails — it currently prints to the console
- `CALL_VERIFICATION_PROVIDER_SID` / `_TOKEN` / `_FROM_NUMBER` — wire to Exotel/Twilio Voice/etc. in `accounts/utils.py::place_verification_call`

## API map

| Area | Base path |
|---|---|
| Auth (register/login/logout, 3 user types) | `/api/auth/` |
| Menu (categories, sub-categories, items) | `/api/menu/` |
| Cart, checkout, wishlist, order history | `/api/orders/` |
| Delivery profile + live location | `/api/delivery/` |
| Razorpay payment verification | `/api/payments/` |
| Contact form + admin live monitor | `/api/core/` |
| Django admin | `/admin/` |

Full endpoint list is in each app's `api_urls.py`.

## What's been tested and confirmed working

- Customer / client / delivery registration and login (separate endpoints, separate redirects, shared `User` table via `user_type`)
- Client creating a menu item under their own `ClientProfile` (permission-checked — a client can't edit another client's items)
- Menu browsing with category/subcategory nesting, `mode=online|offline` filter, search
- Add to cart → checkout with Cash on Delivery → confirmation email sent → order shows in order history
- Age-restricted item + unverified customer age → checkout correctly branches into `pending_age_verification`, creates the call-verification tracking record instead of silently blocking or silently allowing the order
- Contact form → acknowledgment email sent

Razorpay order-creation code is written against the real SDK and shaped
correctly (`payments/utils.py`), but wasn't hit against Razorpay's live API
in this sandbox (no network egress to Razorpay from here, and no real keys)
— plug in your test keys and it should work as written.

## What's next (not yet in this drop)

1. **Frontend**: Bootstrap5 responsive templates for home, menu (with veg/non-veg/international filter chips), cart, contact, and the 6 register/login pages (customer/client/delivery), plus `static/js/main.js` with the async/await + Promise-based fetch calls, hover/onclick handlers, toast messages, and redirect logic; a three.js hero visual.
2. **Client dashboard** — manage own menu items, see incoming orders, update order status.
3. **Delivery dashboard** — accept orders, push live location via `navigator.geolocation`.
4. **Admin live-monitoring UI** — a page consuming `/api/core/admin/live-monitor/`, ideally upgraded to WebSockets (Django Channels) instead of polling for true real-time tracking.
5. **Wishlist UI**, **user location autofill** (browser geolocation → reverse geocode → `delivery_address`).
6. **Mobile app**: this API is already CORS-enabled and token-auth-capable, so a React Native / Flutter app can consume it directly without backend changes.
