# HBooking – Django Travel Booking

Full-stack travel booking web app: **Django** backend (models, auth, booking workflow) and **Django templates** (HTML, CSS, JS) for the frontend.

## Folder structure

```
hbooking/
├── manage.py                 # Django CLI
├── requirements.txt
├── db.sqlite3                # SQLite DB (created after migrate)
├── hbooking/                 # Project config
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/                  # Custom user, login/register, dashboard
│   ├── models.py             # User (email as USERNAME_FIELD)
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
├── locations/                 # State & City, AJAX cities by state
│   ├── models.py             # State, City(FK State)
│   ├── views.py              # cities_by_state JSON
│   └── urls.py
├── trips/                     # Trip CRUD, search, detail
│   ├── models.py             # Trip (transport_type, source/dest city, date, time, seats, price)
│   ├── views.py              # home, search, trip_detail
│   └── urls.py
├── bookings/                  # Booking creation, seat validation, email
│   ├── models.py             # Booking (user, trip, seats, total_price, is_paid)
│   ├── views.py              # create_booking (atomic), _send_booking_confirmation
│   └── urls.py
├── payments/                  # Simulated payment, confirmation
│   ├── models.py             # Payment (booking, amount, transaction_id)
│   ├── views.py              # payment, success (mark paid, send email)
│   └── urls.py
├── templates/                 # Global + app templates
│   ├── base.html
│   ├── trips/                # home, search, trip_detail
│   ├── accounts/             # login, register, dashboard
│   ├── bookings/             # (redirects; no dedicated booking template)
│   └── payments/             # payment, success
└── static/
    ├── css/style.css
    └── js/main.js
```

## Commands to run locally

1. **Create and activate a virtual environment (recommended)**

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Migrations**

   ```bash
   python manage.py makemigrations accounts locations trips bookings payments
   python manage.py migrate
   ```

4. **Create a superuser (optional, for admin)**

   ```bash
   python manage.py createsuperuser
   ```
   Use an **email** as the username.

5. **Load sample data (optional)**

   ```bash
   python manage.py load_sample_locations
   ```
   This creates sample states (e.g. Maharashtra, Karnataka), cities (Mumbai, Pune, Bengaluru), and trips for the next day. You can also create data via Django admin: `http://127.0.0.1:8000/admin/`.

6. **Run the dev server**

   ```bash
   python manage.py runserver
   ```

7. **Open in browser**

   - Home: `http://127.0.0.1:8000/`
   - Search (Services): `http://127.0.0.1:8000/search/`
   - Login: `http://127.0.0.1:8000/accounts/login/`
   - Register: `http://127.0.0.1:8000/accounts/register/`
   - After login, dashboard: `http://127.0.0.1:8000/accounts/dashboard/`

## Features

- **Phase 1:** Django project, apps (accounts, locations, trips, bookings, payments), SQLite, custom user (email login).
- **Phase 2:** Homepage with Bus / Train / Flight cards and navbar (Home, Services, Login, Logout, Register).
- **Phase 3:** State & City models; dynamic city dropdown via AJAX (select state → load cities).
- **Phase 4:** Trip model and search form (transport, source/destination, date); results list.
- **Phase 5:** Booking with seat selection, availability check, and atomic transaction.
- **Phase 6:** Payment simulation page; booking confirmed only after “Pay Now” success.
- **Phase 7:** Email confirmation sent when booking is paid (console backend in dev).
- **Phase 8:** User dashboard with booking history and pay link for unpaid bookings.
- **Phase 9:** Responsive UI with gradients, hover effects, and basic animations.

## Email

In development, emails are printed to the console. Set `EMAIL_BACKEND` and SMTP in `settings.py` for production.
