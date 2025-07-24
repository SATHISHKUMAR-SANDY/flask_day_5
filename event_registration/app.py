from flask import Flask, render_template, redirect, url_for, flash
from config import Config
from models import db, Attendee
from forms import AttendeeForm

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return redirect(url_for('list_attendees'))

@app.route('/attendees')
def list_attendees():
    attendees = Attendee.query.all()
    return render_template('attendees.html', attendees=attendees)

@app.route('/add', methods=['GET', 'POST'])
def add_attendee():
    form = AttendeeForm()
    if form.validate_on_submit():
        # Check for duplicate email
        if Attendee.query.filter_by(email=form.email.data).first():
            flash("Email already registered.", "danger")
            return render_template('attendee_form.html', form=form, title="Add Attendee")
        attendee = Attendee(
            name=form.name.data,
            email=form.email.data,
            event_name=form.event_name.data
        )
        db.session.add(attendee)
        db.session.commit()
        flash("Attendee registered successfully!", "success")
        return redirect(url_for('list_attendees'))
    return render_template('attendee_form.html', form=form, title="Add Attendee")

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_attendee(id):
    attendee = Attendee.query.get_or_404(id)
    form = AttendeeForm(obj=attendee)
    if form.validate_on_submit():
        # Check email uniqueness only if changed
        if attendee.email != form.email.data:
            if Attendee.query.filter_by(email=form.email.data).first():
                flash("Email already registered.", "danger")
                return render_template('attendee_form.html', form=form, title="Edit Attendee")
        attendee.name = form.name.data
        attendee.email = form.email.data
        attendee.event_name = form.event_name.data
        db.session.commit()
        flash("Attendee updated successfully!", "info")
        return redirect(url_for('list_attendees'))
    return render_template('attendee_form.html', form=form, title="Edit Attendee")

@app.route('/delete/<int:id>')
def delete_attendee(id):
    attendee = Attendee.query.get_or_404(id)
    db.session.delete(attendee)
    db.session.commit()
    flash("Attendee deleted successfully!", "warning")
    return redirect(url_for('list_attendees'))

if __name__ == '__main__':
    app.run(debug=True)
