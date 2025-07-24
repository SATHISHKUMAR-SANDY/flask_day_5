from flask import Flask, render_template, redirect, url_for, flash
from config import Config
from models import db, User
from forms import UserForm

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Create tables safely for Python 3.13+
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/create', methods=['GET', 'POST'])
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash('User created successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('create_user.html', form=form)

@app.route('/update/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.commit()
        flash('User updated successfully!', 'info')
        return redirect(url_for('index'))
    return render_template('update_user.html', form=form)

@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
