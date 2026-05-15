CREATE TABLE movie (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    genre VARCHAR(50) NOT NULL,
    ticket_price FLOAT NOT NULL,
    created_at DATETIME
);

CREATE TABLE showtime (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    movie_id INTEGER NOT NULL,
    theater_name VARCHAR(100) NOT NULL,
    show_date VARCHAR(20) NOT NULL,
    show_time VARCHAR(20) NOT NULL,
    created_at DATETIME,
    FOREIGN KEY (movie_id) REFERENCES movie(id)
);

CREATE TABLE booking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name VARCHAR(100) NOT NULL,
    customer_email VARCHAR(120) NOT NULL,
    showtime_id INTEGER NOT NULL,
    ticket_quantity INTEGER NOT NULL,
    total_amount FLOAT NOT NULL,
    created_at DATETIME,
    FOREIGN KEY (showtime_id) REFERENCES showtime(id)
);

CREATE TABLE payment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    payment_status VARCHAR(50) NOT NULL,
    paid_amount FLOAT NOT NULL,
    created_at DATETIME,
    FOREIGN KEY (booking_id) REFERENCES booking(id)
);