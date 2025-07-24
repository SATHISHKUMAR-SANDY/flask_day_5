from flask import Flask, render_template, redirect, url_for, flash
from config import Config
from models import db, Contact
from forms import ContactForm

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return redirect(url_for('list_contacts'))

@app.route('/contacts')
def list_contacts():
    contacts = Contact.query.order_by(Contact.name).all()
    return render_template('contacts.html', contacts=contacts)

@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Check for existing email or phone to avoid duplicates
        existing_email = Contact.query.filter_by(email=form.email.data).first()
        existing_phone = Contact.query.filter_by(phone=form.phone.data).first()
        if existing_email:
            flash("Email already exists.", "danger")
            return render_template('contact_form.html', form=form, title="Add Contact")
        if existing_phone:
            flash("Phone number already exists.", "danger")
            return render_template('contact_form.html', form=form, title="Add Contact")

        contact = Contact(
            name=form.name.data,
            phone=form.phone.data,
            email=form.email.data,
            address=form.address.data
        )
        db.session.add(contact)
        db.session.commit()
        flash("Contact added successfully!", "success")
        return redirect(url_for('list_contacts'))
    return render_template('contact_form.html', form=form, title="Add Contact")

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):
    contact = Contact.query.get_or_404(id)
    form = ContactForm(obj=contact)
    if form.validate_on_submit():
        # Check if email or phone changed to existing in other records
        existing_email = Contact.query.filter(Contact.email==form.email.data, Contact.id!=id).first()
        existing_phone = Contact.query.filter(Contact.phone==form.phone.data, Contact.id!=id).first()
        if existing_email:
            flash("Email already exists.", "danger")
            return render_template('contact_form.html', form=form, title="Edit Contact")
        if existing_phone:
            flash("Phone number already exists.", "danger")
            return render_template('contact_form.html', form=form, title="Edit Contact")

        contact.name = form.name.data
        contact.phone = form.phone.data
        contact.email = form.email.data
        contact.address = form.address.data
        db.session.commit()
        flash("Contact updated successfully!", "info")
        return redirect(url_for('list_contacts'))
    return render_template('contact_form.html', form=form, title="Edit Contact")

@app.route('/delete/<int:id>')
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    flash("Contact deleted successfully!", "warning")
    return redirect(url_for('list_contacts'))

if __name__ == '__main__':
    app.run(debug=True)
