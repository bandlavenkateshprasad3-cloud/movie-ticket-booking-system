# Database Normalization Report

## Original Functional Dependencies

### Movie
- movie_id → title, genre, ticket_price

### Showtime
- showtime_id → movie_id, theater_name, show_date, show_time

### Booking
- booking_id → customer_name, customer_email, showtime_id, ticket_quantity, total_amount

### Payment
- payment_id → booking_id, payment_method, payment_status, paid_amount

---

## Anomaly Identification

### Update Anomaly
If movie information was stored repeatedly with showtime records, updating movie details would require multiple updates.

### Insertion Anomaly
Without normalization, adding a booking could require unnecessary repeated movie information.

### Deletion Anomaly
Deleting a booking could accidentally remove payment information if stored together.

---

## Decomposition Steps

The database was decomposed into separate tables:

- Movie
- Showtime
- Booking
- Payment

Relationships were established using foreign keys.

---

## Final Relational Schema

### Movie
- id (PK)
- title
- genre
- ticket_price
- created_at

### Showtime
- id (PK)
- movie_id (FK)
- theater_name
- show_date
- show_time
- created_at

### Booking
- id (PK)
- customer_name
- customer_email
- showtime_id (FK)
- ticket_quantity
- total_amount
- created_at

### Payment
- id (PK)
- booking_id (FK)
- payment_method
- payment_status
- paid_amount
- created_at

---

## Normal Form

The database satisfies Third Normal Form (3NF):
- No repeating groups
- No partial dependencies
- No transitive dependencies