from flask import Flask, render_template, abort
from models import db, User, Product, Blog
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()
    # Add some dummy data if tables are empty
    if not User.query.first():
        dummy_users = [
            User(name="Alice", email="alice@example.com"),
            User(name="Bob", email="bob@example.com"),
        ]
        dummy_products = [
            Product(name="Laptop", price=1200.50, in_stock=True),
            Product(name="Phone", price=799.99, in_stock=False),
        ]
        dummy_blogs = [
            Blog(title="First Blog", content="Content of first blog"),
            Blog(title="Second Blog", content="Content of second blog"),
        ]
        db.session.add_all(dummy_users + dummy_products + dummy_blogs)
        db.session.commit()

@app.route('/users')
def users():
    users = User.query.all()  # 1. Query all users
    return render_template('users.html', users=users)

@app.route('/user/<int:id>')
def user_detail(id):
    user = User.query.get(id)  # 2. Query one user by ID
    if not user:
        abort(404)
    return render_template('user_detail.html', user=user)

@app.route('/user-by-email/<email>')
def user_by_email(email):
    user = User.query.filter_by(email=email).first()  # 3. Filter by email
    if not user:
        abort(404)
    return render_template('user_detail.html', user=user)

@app.route('/products-in-stock')
def products_in_stock():
    products = Product.query.filter_by(in_stock=True).all()  # 4. Products with in_stock=True
    return render_template('products.html', products=products)

@app.route('/blogs')
def blogs():
    blogs = Blog.query.order_by(Blog.created_at.desc()).all()  # 5. Blogs ordered by date descending
    return render_template('blogs.html', blogs=blogs)

@app.route('/user-count')
def user_count():
    count = User.query.count()  # 6. Count total users
    return f"Total users in DB: {count}"

@app.route('/user-dict/<int:id>')
def user_dict(id):
    user = User.query.get(id)
    if not user:
        abort(404)
    # 10. Convert query result to dictionary and print/log it
    user_dict = user.to_dict()
    print(user_dict)  # Here, just printing to console
    return user_dict  # Flask will jsonify dict automatically

if __name__ == '__main__':
    app.run(debug=True)
