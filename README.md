#  Join Backend (Django REST API)

This repository contains the **backend** for the "Join" application.  
The backend is built with **Django Rest Framework (DRF)** and provides a **REST API** for managing tasks (`Tasks`), subtasks (`Subtasks`), and contacts (`Contacts`).

---

## ** Features**
✔ **User authentication** (Registration, Login, Token Authentication)  
✔ **CRUD operations for tasks & contacts**  
✔ **Guest user support (no login required)**  
✔ **CORS handling for secure API access**  
✔ **SQLite (Development) & PostgreSQL (Production) support**  
✔ **Environment variable (`.env`) support for configuration**  

---

## ** Project Structure**
join_backend/
│── api/ # Main app with API endpoints
│── user_auth_app/ # User authentication & management app
│── join_backend/ # Main project settings
│── env/ # Virtual environment (NOT included in Git)
│── manage.py # Django management script
│── .env # Environment variables (IGNORED in Git)
│── requirements.txt # Dependencies for installation
│── README.md # This file
│── db.sqlite3 # SQLite database (for development only)

yaml
Kopieren
Bearbeiten

---

## ** Installation**
### ** Clone the repository**
```bash
git clone git@github.com:OgulcanErdag/join_backend.git
cd join_backend