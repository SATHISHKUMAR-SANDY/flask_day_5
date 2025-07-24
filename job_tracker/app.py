from flask import Flask, render_template, redirect, url_for, flash
from config import Config
from models import db, Application
from forms import ApplicationForm

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    applications = Application.query.all()
    return render_template('index.html', applications=applications)

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    form = ApplicationForm()
    if form.validate_on_submit():
        application = Application(
            name=form.name.data,
            email=form.email.data,
            job_title=form.job_title.data,
            status=form.status.data
        )
        db.session.add(application)
        try:
            db.session.commit()
            flash('Application submitted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error: Email already exists or database issue.', 'danger')
        return redirect(url_for('index'))
    return render_template('application_form.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
