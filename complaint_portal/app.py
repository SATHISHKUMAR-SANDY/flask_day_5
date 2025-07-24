from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from forms import ComplaintForm
from models import db, Complaint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///complaints.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    total = Complaint.query.count()
    resolved = Complaint.query.filter_by(resolved=True).count()
    complaints = Complaint.query.order_by(Complaint.id.desc()).all()
    return render_template('complaint_list.html', complaints=complaints, total=total, resolved=resolved)

@app.route('/submit', methods=['GET', 'POST'])
def submit_complaint():
    form = ComplaintForm()
    if form.validate_on_submit():
        complaint = Complaint(
            name=form.name.data,
            message=form.message.data,
            resolved=False
        )
        db.session.add(complaint)
        db.session.commit()
        flash('Complaint submitted successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('complaint_form.html', form=form)

@app.route('/resolve/<int:id>', methods=['POST'])
def resolve_complaint(id):
    complaint = Complaint.query.get_or_404(id)
    complaint.resolved = True
    db.session.commit()
    flash('Complaint marked as resolved.', 'success')
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_complaint(id):
    complaint = Complaint.query.get_or_404(id)
    db.session.delete(complaint)
    db.session.commit()
    flash('Complaint deleted.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
