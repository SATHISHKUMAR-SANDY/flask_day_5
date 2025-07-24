from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from models import db, User, Product, Blog
from forms import BlogForm, UserForm, ProductForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    users = User.query.all()
    products = Product.query.all()
    blogs = Blog.query.order_by(Blog.created_at.desc()).all()
    return render_template('index.html', users=users, products=products, blogs=blogs)

# 3. Form to create new blog post
@app.route('/create-blog', methods=['GET', 'POST'])
def create_blog():
    form = BlogForm()
    if form.validate_on_submit():
        blog = Blog(title=form.title.data, content=form.content.data)
        try:
            db.session.add(blog)
            db.session.commit()  # 8. commit flow: changes saved in DB here
            flash("Blog created successfully!", "success")  # 10.
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error creating blog: {e}", "danger")
    return render_template('blog_form.html', form=form)

# 4. Route to add dummy users/products for testing
@app.route('/add-dummy')
def add_dummy():
    try:
        user1 = User(name="John Doe", email="john@example.com")
        user2 = User(name="Jane Smith", email="jane@example.com")
        product1 = Product(name="Sample Product", price=9.99)
        product2 = Product(name="Another Product", price=19.99, in_stock=False)
        db.session.add_all([user1, user2, product1, product2])
        db.session.commit()
        flash("Dummy users and products added.", "success")
    except IntegrityError:
        db.session.rollback()
        flash("Dummy data already exists or duplicate emails.", "warning")
    except Exception as e:
        db.session.rollback()
        flash(f"Error adding dummy data: {e}", "danger")
    return redirect(url_for('index'))

# 5. Bulk insert 5 users
@app.route('/bulk-insert')
def bulk_insert():
    users = [
        User(name=f'User{i}', email=f'user{i}@example.com') for i in range(1, 6)
    ]
    try:
        db.session.bulk_save_objects(users)
        db.session.commit()
        flash("Bulk insert of 5 users successful.", "success")
    except IntegrityError:
        db.session.rollback()
        flash("Duplicate email detected during bulk insert.", "warning")
    except Exception as e:
        db.session.rollback()
        flash(f"Error during bulk insert: {e}", "danger")
    return redirect(url_for('index'))

# 6. Add user from form (handles create operation)
@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash("User added successfully!", "success")
            return redirect(url_for('index'))
        except IntegrityError:
            db.session.rollback()
            flash("Email already exists!", "danger")
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding user: {e}", "danger")
    return render_template('user_form.html', form=form)

# 6. Add product from form (in_stock defaults to True)
@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data, price=form.price.data)
        try:
            db.session.add(product)
            db.session.commit()
            flash("Product added successfully!", "success")
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding product: {e}", "danger")
    return render_template('product_form.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
