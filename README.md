# AuctionHub 🔨

AuctionHub is a modern, real-time web application for managing online auctions, built with **Django 6** and powered by **Celery & Redis** for background tasks. It supports role-based user management, live bidding tracking, and automated auction closing.

---

## 🏗️ Project Architecture & Features

The project is structured into modular Django applications:
- **`accounts`**: Custom user accounts with roles: `Buyer`, `Seller`, and `Admin`.
- **`auctions`**: High-level bidding and auction logic supporting:
  - **Timed Auctions**: Conclude automatically at a specified date/time. Checked dynamically via background tasks.
  - **Open Auctions**: Open for bidding until manually closed by the seller.
  - **AJAX Updates**: Frontend client polls `/auctions/<pk>/status/` dynamically to synchronize bid values without page reloads.
- **`products`**: Product listings, categories, active toggles, and image uploads.
- **`payments`**: Placeholder structure for transaction processing and checkouts.

---

## 🛠️ Technology Stack & Requirements

### Required Software
- **Python**: `3.11.9` (specified in `runtime.txt`)
- **Redis Server**: Required as the message broker for Celery tasks.
- **PostgreSQL**: Optional for production environment (SQLite is configured as default local fallback).

### Backend & Libraries
- **Django**: `6.0.6`
- **Celery & Django-Celery-Beat**: Background task runner & scheduler for expiring auctions.
- **Bootstrap 5 & Django-Crispy-Forms**: Responsive design & stylized user forms.
- **WhiteNoise & Gunicorn**: Prepared for seamless production deployment (e.g., Render/Heroku).

---

## 🚀 Getting Started

Follow these steps to set up the project on a new machine:

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/auctionhub.git
cd auctionhub
```

### 2. Set Up the Virtual Environment
Ensure you have Python 3.11 installed. Initialize and activate the virtual environment:
```bash
# Windows
python -m venv env
.\env\Scripts\activate

# macOS / Linux
python3 -m venv env
source env/bin/activate
```

### 3. Install Dependencies
Install all package requirements listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the template configuration file:
```bash
cp .env.example .env
```
Open `.env` and configure your credentials.

### 5. Run Database Migrations
Initialize your local database schemas:
```bash
python manage.py migrate
```

### 6. Create an Admin Account
To manage products and access Django Admin console:
```bash
python manage.py createsuperuser
```

---

## ⚙️ Running the Services

AuctionHub relies on three main services running simultaneously:

### 1. Django Web Server
Start the Django development server:
```bash
python manage.py runserver
```
Access the application at `http://127.0.0.1:8000/`.

### 2. Redis Message Broker
Ensure your Redis instance is running locally.
```bash
# On Linux/macOS:
redis-server

# On Windows (if installed via WSL/native):
sudo service redis-server start
```

### 3. Celery Worker (Task Executor)
In a new terminal window (with virtual environment activated), start the worker to execute tasks:
```bash
celery -A auction_site worker --loglevel=info
```

### 4. Celery Beat (Task Scheduler)
In another terminal window (with virtual environment activated), start the scheduler to queue the periodic auction-expiration checks:
```bash
celery -A auction_site beat --loglevel=info
```
*Note: The background task `close_expired_auctions` is configured to run every minute.*

---

## 📂 Codebase Overview

```bash
auction_app/
│
├── auction_site/       # Project settings, URL routing, and Celery configuration
├── accounts/           # User models (custom Roles), views, forms, and auth handlers
├── products/           # Categories, product details, and image uploads
├── auctions/           # Auction instances, bids, status endpoints, and background tasks
├── payments/           # Structure for payment processor integration
│
├── templates/          # HTML templates styled with Crispy Forms and Bootstrap 5
├── requirements.txt    # Python packages
├── Procfile            # Deployment script for web dynos
└── db.sqlite3          # Development database
```

---

## 🔮 Future Enhancements & TODOs
If you are taking over this codebase, consider completing the following modules:
1. **Payments System**: Implement views and models in the `payments/` application (e.g., Stripe, PayPal, Razorpay integrations).
2. **WebSocket Support**: Replace AJAX polling in `auctions/views.py` (`auction_status` endpoint) with WebSockets using **Django Channels** for real-time bid broadcasts.
3. **Email Notification Service**: Hook into celery tasks to email the winning bidder when an auction closes.
