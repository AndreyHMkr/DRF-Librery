# 📚 DRF Library Project

This is a Django REST API for a library system with the following features:

- Book listing and borrowing
- Stripe payments integration
- Telegram notifications
- Swagger/OpenAPI documentation
- Periodic tasks using Celery & Beat

---

## 🚀 Getting Started

### 🔧 Requirements

- Stripe account
- Telegram bot

### ⚙️ Environment Variables (`.env`)

```
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_SUCCESS_URL=http://127.0.0.1:8000/success/
STRIPE_CANCEL_URL=http://127.0.0.1:8000/cancel/
TG_BOT_TOKEN=your_telegram_token
TG_CHAT_ID=your_admin_chat_id
DEBUG=True
```

---

## 🖥️ Run the Project

1. **Apply Migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

2. **Create Superuser**

```bash
python manage.py createsuperuser
```

3. **Start Django Server**

```bash
python manage.py runserver
```

---

## ⏱ Celery Tasks

Used for overdue borrowings check.

### 🔁 Start Celery Beat

```bash
celery -A DRF_Library beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

### ⚙️ Start Celery Worker

```bash
celery -A DRF_Library worker -l info --pool=solo
```

---

## 📬 Telegram Notifications

- Sent when:
    - a borrowing is created
    - a book is returned
    - a borrowing is overdue

---

## 💳 Stripe Integration

- Payment session is created on borrowing
- Success and cancel URLs handle payment status:
    - `/success/`
    - `/cancel/`

---

## 📘 API Documentation

### Swagger UI:

```
http://127.0.0.1:8000/api/doc/swagger/
```

### Redoc:

```
http://127.0.0.1:8000/api/doc/redoc/
```

---

## 📌 Main Endpoints

| Endpoint          | Description              |
|-------------------|--------------------------|
| `/api/books/`     | List and create books    |
| `/api/borrowing/` | Manage borrowings        |
| `/api/payments/`  | View user/admin payments |
| `/success/`       | Stripe success URL       |
| `/cancel/`        | Stripe cancel URL        |

---

## 🧪 Run Tests

```bash
python manage.py test
```
