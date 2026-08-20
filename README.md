# FoodVibe — Online Food Ordering & Delivery Platform

A modern, startup-ready, full-stack **Food Ordering Platform** built with **Django**, **Django REST Framework (DRF)**, **Bootstrap 5**, **vanilla JavaScript (async/await, Promises, Toasts, Geolocation)**, and an interactive **Three.js 3D hero visualization**.

---

## 🌟 Key Features

### 1. Multi-Role Portals & Separate Auth Flows
- **Customer Portal**: Dedicated Register & Login, Cart, Wishlist, Order History & Live 5-stage tracking timeline.
- **Restaurant / Hotel Partner Portal**: Dedicated Register & Login, Live Kitchen Queue, Menu Management CRUD (modal), Online/Offline toggle.
- **Delivery Partner Portal**: Dedicated Register & Login, Live GPS Beacon broadcaster (`navigator.geolocation.watchPosition`), Delivery run updater.
- **Admin Live Monitoring Console**: Live order telemetry, revenue stats, active rider radar coordinates, and session/cookie diagnostics.

### 2. 4 Core Food Categories & Regional Indian Choices
1. **Pure Vegetarian**: Dal Makhani, Dosa, Thali, Biryani.
2. **Non-Vegetarian**: Butter Chicken, Kashmiri Rogan Josh, Tandoori Chicken, Hyderabadi Dum Biryani.
3. **International**: Artisan Pizzas, Fettuccine Alfredo, Hakka Noodles, Double Cheeseburgers.
4. **Indian Regional Paneer Varieties**: Matar Paneer, Aloo Paneer, Chilli Paneer, Palak Paneer, Paneer Tikka.

### 3. Interactive Frontend
- **Three.js 3D Interactive Hero Canvas**: Rotating 3D gourmet burger platter with dynamic lighting, melting cheese, lettuce, tomato, sesame seeds, floating ambient ingredient particles, and mouse/touch drag controls.
- **Async Client (Promises & Fetch)**: Dynamic cart badge counter, 1-click GPS Geolocation auto-fill, toast alerts, and 18+ age verification popup prompt.

---

## 🚀 Quick Setup & Run

```bash
cd foodapp

# 1. Install dependencies
pip install -r requirements.txt

# 2. Run migrations
python manage.py migrate

# 3. Seed menu categories & realistic test dishes + accounts
python manage.py seed_menu
python manage.py seed_sample_dishes

# 4. Start the development server
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

---

## 🔑 Pre-Seeded Test Accounts

| Role | Username | Password | Dashboard URL |
|---|---|---|---|
| **Admin Superuser** | `admin` | `admin123` | `/live-monitor/` or `/admin/` |
| **Customer** | `customer_john` | `customer123` | `/` and `/menu/` |
| **Restaurant Partner** | `taj_hotel` | `client123` | `/client/dashboard/` |
| **Delivery Rider** | `rider_vikram` | `delivery123` | `/delivery/dashboard/` |

---

## 📡 REST API Map

| Area | Base Path | Description |
|---|---|---|
| **Auth** | `/api/auth/` | Customer, Client, Delivery register/login/logout endpoints |
| **Menu** | `/api/menu/` | Categories, subcategories, items CRUD & filtering |
| **Orders** | `/api/orders/` | Cart management, checkout, wishlist, order history |
| **Delivery** | `/api/delivery/` | Delivery profile & live GPS location updates |
| **Payments** | `/api/payments/` | Razorpay signature verification & webhook hooks |
| **Live Telemetry** | `/api/core/` | Contact messages & Admin live monitor |

---

## 🧪 Testing

Run the automated test suite:
```bash
python manage.py test
```
*All 6 unit & integration tests pass with 100% success.*
