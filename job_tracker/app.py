from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from models import db, Application
from forms import ApplicationForm

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Create tables once when app starts
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return redirect(url_for('list_applications'))

@app.route('/applications')
def list_applications():
    status_filter = request.args.get('status')
    if status_filter in ['applied', 'shortlisted', 'rejected']:
        applications = Application.query.filter_by(status=status_filter).order_by(Application.id.desc()).all()
    else:
        applications = Application.query.order_by(Application.id.desc()).all()
    return render_template('applications.html', applications=applications, status_filter=status_filter)

@app.route('/add', methods=['GET', 'POST'])
def add_application():
    form = ApplicationForm()
    if form.validate_on_submit():
        existing_email = Application.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash("An application with this email already exists.", "danger")
            return render_template('application_form.html', form=form, title="Add Application")
        application = Application(
            name=form.name.data,
            email=form.email.data,
            job_title=form.job_title.data,
            status=form.status.data
        )
        db.session.add(application)
        db.session.commit()
        flash("Application added successfully!", "success")
        return redirect(url_for('list_applications'))
    return render_template('application_form.html', form=form, title="Add Application")

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_application(id):
    application = Application.query.get_or_404(id)
    form = ApplicationForm(obj=application)
    if form.validate_on_submit():
        if form.email.data != application.email:
            existing_email = Application.query.filter(Application.email == form.email.data, Application.id != id).first()
            if existing_email:
                flash("Email already used by another application.", "danger")
                return render_template('application_form.html', form=form, title="Edit Application")
        application.name = form.name.data
        application.email = form.email.data
        application.job_title = form.job_title.data
        application.status = form.status.data
        db.session.commit()
        flash("Application updated successfully!", "info")
        return redirect(url_for('list_applications'))
    return render_template('application_form.html', form=form, title="Edit Application")

@app.route('/delete/<int:id>')
def delete_application(id):
    application = Application.query.get_or_404(id)
    db.session.delete(application)
    db.session.commit()
    flash("Application deleted successfully!", "warning")
    return redirect(url_for('list_applications'))

if __name__ == '__main__':
    app.run(debug=True)
