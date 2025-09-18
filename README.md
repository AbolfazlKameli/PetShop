# PetShop

PetShop is a robust and scalable backend solution designed with Django and Django REST Framework (DRF). It includes
authentication, task management, and cloud storage integration.

---

## 🚀 Features

- **🔑 JWT Authentication** – Secure API access with JSON Web Tokens.
- **📖 DRF Spectacular** – Automatic OpenAPI/Swagger documentation generation.
- **🛢️ PostgreSQL Database** – Reliable and scalable relational database.
- **⚡ Redis for Caching** – High-performance caching for optimized API responses.
- **📩 Redis as Celery Message Broker** – Efficient task queue management with Celery.
- **☁️ Arvan Cloud Storage Integration** – Scalable and efficient cloud storage.
- **⏳ Celery** – Asynchronous task execution for background processes.
- **👤 Custom User Model** – Flexible authentication with extended functionality.
- **🔄 Two-Step Registration** – Secure registration flow with activation email.
- **📧 SMTP Configuration** – Pre-configured for sending emails via various SMTP services.

---

## 👥 Authors

- [Abolfazl Kameli](https://github.com/AbolfazlKameli) (Back-end Developer)
- [Hosein Parvaresh](https://github.com/HoseinParvaresh) (Front-end Developer)
---

## 🐳 Run with Docker

1. Create your `.env` file:
   ```sh
   cp example.env .env
   ```

2. Build and run the project based on the environment:

   **For development:**
   ```sh
   docker compose -f docker-compose.dev.yml up --build
   ```

   **For production:**
   ```sh
   docker compose -f docker-compose.yml up --build
   ```

---

## 💻 Run Locally

### 1️⃣ Install Required Packages

- Install Redis by following
  the [installation guide](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/).

### 2️⃣ Clone the Project

```sh
$ git clone https://github.com/AbolfazlKameli/PetShop
```

### 3️⃣ Navigate to the Project Directory

```sh
$ cd PetShop
```

### 4️⃣ Create & Activate a Virtual Environment

```sh
$ python3 -m venv .venv
$ source .venv/bin/activate
```

### 5️⃣ Install Dependencies

```sh
$ pip install -r requirements.txt
```

### 6️⃣ Set Up Environment Variables

```sh
$ cp example.env .env
```

### 7️⃣ Apply Database Migrations

```sh
$ python manage.py makemigrations
$ python manage.py migrate
```

### 8️⃣ Start the Django Server

```sh
$ python manage.py runserver
```

---

## 🔧 Basic Commands

### 📌 Create a Superuser

```sh
$ python manage.py createsuperuser
```

### ⚙️ Run Celery Worker

```sh
$ celery -A config worker -l INFO
```

_Ensure you run this command in the same directory as `manage.py`._

---

Enjoy coding! 🚀
