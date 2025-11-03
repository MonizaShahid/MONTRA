# MONTRA Django Project

A Django-based project. This file explains how to install, run, and set up the project.

## ✅ Requirements

* Python 3.x
* Django installed
* Git installed

## 📥 Clone the Project

```
git clone https://github.com/MonizaShahid/MONTRA.git
cd MONTRA
```

## 🧠 Create Virtual Environment

### Windows:

```
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux:

```
python3 -m venv venv
source venv/bin/activate
```

## 📦 Install Dependencies

```
pip install -r requirements.txt
```

If `requirements.txt` is missing, install Django manually:

```
pip install django
```

## ⚙️ Run Migrations

```
python manage.py makemigrations
python manage.py migrate
```

## 👤 Create Superuser (Admin Login)

```
python manage.py createsuperuser
```

## ▶️ Run the Server

```
python manage.py runserver
```

Open browser:

```
http://127.0.0.1:8000/
```

## 📁 Project Structure

```
MONTRA/
 ├── manage.py              # Django manager file
 ├── project_folder/        # Django settings & URLs
 └── app_folder/            # App files (views, models, templates)
```





