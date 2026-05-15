from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime

app = Flask(__name__)
app.secret_key = "movie_project_secret_key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    ticket_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    showtimes = db.relationship('Showtime', backref='movie', cascade='all, delete-orphan')

class Showtime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    theater_name = db.Column(db.String(100), nullable=False)
    show_date = db.Column(db.String(20), nullable=False)
    show_time = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bookings = db.relationship('Booking', backref='showtime', cascade='all, delete-orphan')

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    showtime_id = db.Column(db.Integer, db.ForeignKey('showtime.id'), nullable=False)
    ticket_quantity = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    payment = db.relationship('Payment', backref='booking', uselist=False, cascade='all, delete-orphan')

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(50), nullable=False)
    paid_amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def home():
    movies = Movie.query.all()
    total_movies = Movie.query.count()
    total_showtimes = Showtime.query.count()
    total_bookings = Booking.query.count()

    average_price = db.session.query(func.avg(Movie.ticket_price)).scalar() or 0
    total_revenue = db.session.query(func.sum(Payment.paid_amount)).filter(Payment.payment_status == "Paid").scalar() or 0

    return render_template(
        'index.html',
        movies=movies,
        total_movies=total_movies,
        total_showtimes=total_showtimes,
        total_bookings=total_bookings,
        average_price=round(average_price, 2),
        total_revenue=round(total_revenue, 2)
    )

@app.route('/add', methods=['POST'])
def add_movie():
    title = request.form['title'].strip()
    genre = request.form['genre'].strip()
    ticket_price = float(request.form['ticket_price'])

    if title == "" or genre == "" or ticket_price <= 0:
        flash("Invalid movie data. Please enter valid values.")
        return redirect('/')

    new_movie = Movie(title=title, genre=genre, ticket_price=ticket_price)
    db.session.add(new_movie)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_movie(id):
    movie = Movie.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_movie(id):
    movie = Movie.query.get_or_404(id)

    if request.method == 'POST':
        title = request.form['title'].strip()
        genre = request.form['genre'].strip()
        ticket_price = float(request.form['ticket_price'])

        if title == "" or genre == "" or ticket_price <= 0:
            flash("Invalid movie data. Please enter valid values.")
            return redirect(f'/edit/{id}')

        movie.title = title
        movie.genre = genre
        movie.ticket_price = ticket_price
        db.session.commit()
        return redirect('/')

    return render_template('edit.html', movie=movie)

@app.route('/showtimes')
def showtimes():
    movies = Movie.query.all()
    showtimes = Showtime.query.all()
    return render_template('showtimes.html', movies=movies, showtimes=showtimes)

@app.route('/add_showtime', methods=['POST'])
def add_showtime():
    movie_id = request.form['movie_id']
    theater_name = request.form['theater_name'].strip()
    show_date = request.form['show_date']
    show_time = request.form['show_time']

    if theater_name == "" or show_date == "" or show_time == "":
        flash("Invalid showtime data.")
        return redirect('/showtimes')

    new_showtime = Showtime(
        movie_id=movie_id,
        theater_name=theater_name,
        show_date=show_date,
        show_time=show_time
    )

    db.session.add(new_showtime)
    db.session.commit()
    return redirect('/showtimes')

@app.route('/delete_showtime/<int:id>')
def delete_showtime(id):
    showtime = Showtime.query.get_or_404(id)
    db.session.delete(showtime)
    db.session.commit()
    return redirect('/showtimes')

@app.route('/bookings')
def bookings():
    showtimes = Showtime.query.all()
    bookings = Booking.query.all()
    return render_template('bookings.html', showtimes=showtimes, bookings=bookings)

@app.route('/add_booking', methods=['POST'])
def add_booking():
    customer_name = request.form['customer_name'].strip()
    customer_email = request.form['customer_email'].strip()
    showtime_id = int(request.form['showtime_id'])
    ticket_quantity = int(request.form['ticket_quantity'])
    payment_method = request.form['payment_method']

    showtime = Showtime.query.get_or_404(showtime_id)

    if customer_name == "" or "@" not in customer_email or ticket_quantity <= 0:
        flash("Invalid booking data.")
        return redirect('/bookings')

    total_amount = showtime.movie.ticket_price * ticket_quantity

    try:
        new_booking = Booking(
            customer_name=customer_name,
            customer_email=customer_email,
            showtime_id=showtime_id,
            ticket_quantity=ticket_quantity,
            total_amount=total_amount
        )

        db.session.add(new_booking)
        db.session.flush()

        new_payment = Payment(
            booking_id=new_booking.id,
            payment_method=payment_method,
            payment_status="Paid",
            paid_amount=total_amount
        )

        db.session.add(new_payment)
        db.session.commit()

    except:
        db.session.rollback()
        flash("Transaction failed. Booking was not saved.")

    return redirect('/bookings')

@app.route('/delete_booking/<int:id>')
def delete_booking(id):
    booking = Booking.query.get_or_404(id)
    db.session.delete(booking)
    db.session.commit()
    return redirect('/bookings')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)