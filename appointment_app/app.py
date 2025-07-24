from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from datetime import datetime, date
from forms import AppointmentForm, UpdateStatusForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appointments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

from models import Appointment

# ✅ This replaces @app.before_first_request
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    # Show all upcoming appointments
    today = date.today()
    appointments = Appointment.query.filter(Appointment.date >= today).order_by(Appointment.date, Appointment.time).all()
    return render_template('appointments.html', appointments=appointments)

@app.route('/book', methods=['GET', 'POST'])
def book():
    form = AppointmentForm()
    if form.validate_on_submit():
        new_appointment = Appointment(
            name=form.name.data,
            date=form.date.data,
            time=form.time.data,
            status='Pending'
        )
        db.session.add(new_appointment)
        db.session.commit()
        flash("Appointment booked successfully!", "success")
        return redirect(url_for('home'))
    return render_template('add_appointment.html', form=form)

@app.route('/admin')
def admin():
    # Show all appointments (including past)
    appointments = Appointment.query.order_by(Appointment.date.desc(), Appointment.time.desc()).all()
    return render_template('appointments.html', appointments=appointments, admin=True)

@app.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
def edit_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    form = UpdateStatusForm(obj=appointment)
    if form.validate_on_submit():
        appointment.status = form.status.data
        db.session.commit()
        flash("Appointment status updated!", "success")
        return redirect(url_for('admin'))
    return render_template('edit_appointment.html', form=form, appointment=appointment)

@app.route('/admin/delete/<int:id>', methods=['POST'])
def delete_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    db.session.delete(appointment)
    db.session.commit()
    flash("Appointment deleted!", "success")
    return redirect(url_for('admin'))

if __name__ == "__main__":
    app.run(debug=True)
