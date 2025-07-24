from flask import Flask, render_template, redirect, url_for, flash, request
from models import db, Subscriber
from forms import SubscriberForm
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_456'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///subscribers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    subscribers = Subscriber.query.order_by(Subscriber.subscribed_on.desc()).all()
    return render_template('index.html', subscribers=subscribers)

@app.route('/add', methods=['GET', 'POST'])
def add_subscriber():
    form = SubscriberForm()
    if form.validate_on_submit():
        new_subscriber = Subscriber(
            email=form.email.data,
            plan=form.plan.data,
            subscribed_on=datetime.utcnow()
        )
        db.session.add(new_subscriber)
        db.session.commit()
        flash('Subscriber added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_subscriber.html', form=form)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_subscriber(id):
    subscriber = Subscriber.query.get_or_404(id)
    form = SubscriberForm(obj=subscriber)
    if form.validate_on_submit():
        subscriber.email = form.email.data
        subscriber.plan = form.plan.data
        db.session.commit()
        flash('Subscription updated successfully.', 'success')
        return redirect(url_for('index'))
    return render_template('edit_subscriber.html', form=form)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_subscriber(id):
    subscriber = Subscriber.query.get_or_404(id)
    db.session.delete(subscriber)
    db.session.commit()
    flash('Subscriber deleted.', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
