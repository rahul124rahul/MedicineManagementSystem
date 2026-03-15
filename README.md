# 💊 Medicine Management System

A web-based application built with **Flask** and **MySQL** to manage patients, their prescribed medicines, and dosage schedules in one place.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [API Routes](#api-routes)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [Usage Guide](#usage-guide)

---

## Overview

The Medicine Management System allows healthcare staff or administrators to:

- Register and manage patients (name, age, gender)
- Assign medicines to patients with descriptions
- Track dosage schedules (amount, schedule, start date, end date) per medicine
- View a complete medicine list across all patients
- Navigate a clean dashboard with dedicated sections for Patients and Medicines

---

## Features

| Feature | Description |
|---|---|
| Patient Management | Add, view, edit, and list all patients |
| Medicine Management | Add medicines globally or directly to a specific patient |
| Dose Tracking | Add dosage details (amount, schedule, date range) per medicine |
| Patient Details View | See all medicines and doses assigned to a specific patient |
| Dashboard | Visual landing page with quick navigation cards |
| Cascading Deletes | Deleting a patient removes all linked medicines and doses automatically |
| Optional Assignments | Medicines can exist without being assigned to any patient |

---

## Project Structure

```
MedicineManagementSystem/
│
├── app.py                  # Main Flask application — routes, models, DB init
├── config.py               # Database configuration class
├── requirements.txt        # Python package dependencies
│
├── models/                 # (Reserved for model separation)
│   ├── __init__.py
│   ├── patient.py
│   ├── medicine.py
│   └── dose.py
│
├── templates/              # Jinja2 HTML templates
│   ├── layout.html         # Base template with navbar and dashboard
│   ├── patients.html       # Patient list and add-patient form
│   ├── patient_details.html# Patient profile with medicines and doses
│   ├── edit_patient.html   # Edit patient information
│   └── medicines.html      # Global medicine list and add-medicine form
│
└── static/
    ├── css/
    │   └── style.css       # Application styles
    └── js/
        └── script.js       # Client-side scripts
```

---

## Database Schema

The application uses a **MySQL** database named `medicine_db` with three related tables:

### `patients`
| Column | Type | Description |
|--------|------|-------------|
| id | INT (PK) | Auto-incremented primary key |
| name | VARCHAR(100) | Patient full name |
| age | INT | Patient age |
| gender | VARCHAR(20) | Patient gender |

### `medicines`
| Column | Type | Description |
|--------|------|-------------|
| id | INT (PK) | Auto-incremented primary key |
| name | VARCHAR(100) | Medicine name |
| description | VARCHAR(200) | Optional description |
| patient_id | INT (FK) | Foreign key → `patients.id` (nullable) |

### `doses`
| Column | Type | Description |
|--------|------|-------------|
| id | INT (PK) | Auto-incremented primary key |
| dosage_amount | VARCHAR(100) | Amount per dose (e.g., "500mg") |
| schedule | VARCHAR(100) | Frequency/schedule (e.g., "Twice a day") |
| start_date | VARCHAR(50) | Start date of the dose |
| end_date | VARCHAR(50) | End date of the dose |
| medicine_id | INT (FK) | Foreign key → `medicines.id` |

**Relationships:**
- One `Patient` → Many `Medicines` (cascade delete)
- One `Medicine` → Many `Doses` (cascade delete)

---

## API Routes

### General
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Dashboard / Home page |

### Patient Routes
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/patients` | List all patients |
| POST | `/add_patient` | Add a new patient (with optional medicine and dose) |
| GET | `/patient/<id>` | View patient details, medicines, and doses |
| GET/POST | `/edit_patient/<id>` | Edit an existing patient's information |

### Medicine Routes
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/medicines` | List all medicines |
| POST | `/add_medicine` | Add a new medicine (optionally assign to a patient) |
| POST | `/add_medicine_to_patient/<patient_id>` | Add a medicine directly to a specific patient |

### Dose Routes
| Method | Route | Description |
|--------|-------|-------------|
| POST | `/add_dose/<medicine_id>` | Add a dosage schedule to a specific medicine |

---

## Technologies Used

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.x | Core language |
| Flask | 3.1.3 | Web framework |
| Flask-SQLAlchemy | 3.1.1 | ORM for database interaction |
| SQLAlchemy | 2.0.48 | Database toolkit |
| PyMySQL | 1.1.2 | MySQL driver for Python |
| MySQL | 8.x+ | Relational database |
| Jinja2 | 3.1.6 | HTML templating engine |
| Werkzeug | 3.1.6 | WSGI utilities |

---

## Prerequisites

Before running this application, ensure you have the following installed:

- **Python 3.8+**
- **MySQL Server** (running locally)
- **pip** (Python package manager)
- **Git** (optional)

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd MedicineManagementSystem
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment:

- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Database

Open `app.py` (or `config.py`) and update the database connection string to match your MySQL credentials:

```python
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://<username>:<password>@localhost/medicine_db"
```

Replace `<username>` and `<password>` with your MySQL username and password.

### 5. Create the MySQL Database

Log into MySQL and create the database:

```sql
CREATE DATABASE medicine_db;
```

The application will automatically create all required tables when it starts for the first time.

---

## Running the Application

```bash
python app.py
```

The server will start in debug mode. Open your browser and navigate to:

```
http://127.0.0.1:5000
```

---

## Usage Guide

### Dashboard
The home page provides quick-access cards to navigate to **Patients** or **Medicines**.

### Managing Patients
1. Go to **Patients** from the navbar.
2. Fill in Name, Age, and Gender in the **Add New Patient** form and click **Add Patient**.
3. Click **Show** to view a patient's full profile including their medicines and doses.
4. Click **Edit** to update a patient's name, age, or gender.

### Managing Medicines
1. Go to **Medicines** from the navbar to view and add medicines globally.
2. From a **Patient Details** page, you can add a medicine directly to that patient.
3. When adding a patient, you can optionally include a medicine and dose in the same form.

### Managing Doses
1. Open a **Patient Details** page.
2. For each medicine listed, use the **Add Dose** form to enter:
   - Dosage amount (e.g., `500mg`)
   - Schedule (e.g., `Twice a day after meals`)
   - Start date and End date
3. All doses are displayed under their respective medicine.
