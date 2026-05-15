# Movie Ticket Booking System

## Project Description

This is a full-stack Flask web application developed for CS665 Project 3.

The system allows users to:
- Add movies
- Manage showtimes
- Create ticket bookings
- Process payments
- View dashboard analytics

The application demonstrates CRUD operations, database relationships, transaction logic, and server-side validation using Flask and SQLite.

---

## Technologies Used

- Python 3
- Flask
- SQLAlchemy
- SQLite
- HTML5
- CSS3
- Bootstrap 5
- Jinja2

---

## Features

- Full CRUD Operations
- One-to-Many Relationships
- Booking and Payment Transaction Logic
- Dashboard Analytics
- Data Validation
- Responsive UI

---

## Installation Instructions

### Clone Repository

```bash
git clone <repository-url>
```

### Open Project Folder

```bash
cd movie-ticket-booking-system
```

### Create Virtual Environment

```bash
python3 -m venv venv
```

### Activate Virtual Environment

Mac/Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Application

```bash
python app.py
```

Open browser:

```text
http://127.0.0.1:5000
```

---

## Database Setup

The database is automatically created using SQLAlchemy.

Database file:
- movies.db

SQL schema is included in:
- schema.sql

---

## Main Features

### Movies
- Add movie
- Edit movie
- Delete movie

### Showtimes
- Add showtime
- Delete showtime

### Bookings
- Create booking
- Payment processing
- Delete booking

### Dashboard
- Total Movies
- Total Showtimes
- Total Bookings
- Total Revenue

---

## Git Requirement

Minimum 5 commits are required for submission.
