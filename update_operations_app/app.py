from flask import Flask, render_template, redirect, url_for, flash, request
from models import db, User
from forms import UpdateUserForm
from config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, login_user, current_user, logout_user

import logging

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Setup logging for audit
logging.basicConfig(filename='update_audit.log', level=logging.INFO, format='%(asctime)s %(message)s')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()
    # Create a test user if none exists
    if not User.query.first():
        user = User(username='testuser', email='test@example.com')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('users'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/user/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    user = User.query.get_or_404(id)

    # Only allow the logged-in user to edit their own profile (optional)
    if user.id != current_user.id:
        flash('You can only edit your own profile.', 'danger')
        return redirect(url_for('users'))

    form = UpdateUserForm(original_username=user.username, original_email=user.email, obj=user)

    if form.validate_on_submit():
        before_update = f"Before Update - username: {user.username}, email: {user.email}"

        # Update username and email
        user.username = form.username.data
        user.email = form.email.data

        # Password change logic
        if form.current_password.data:
            if not user.check_password(form.current_password.data):
                flash('Current password is incorrect.', 'danger')
                return render_template('edit_user.html', form=form, user=user)
            if form.new_password.data:
                user.set_password(form.new_password.data)

        db.session.commit()

        after_update = f"After Update - username: {user.username}, email: {user.email}"
        logging.info(f"User ID {user.id} updated.\n{before_update}\n{after_update}")

        flash('Your profile has been updated!', 'success')
        return redirect(url_for('users'))

    return render_template('edit_user.html', form=form, user=user)

if __name__ == '__main__':
    app.run(debug=True)
