from flask import Flask, render_template, redirect, url_for, flash
from config import Config
from models import db, Product
from forms import ProductForm

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    products = Product.query.order_by(Product.id.desc()).all()
    in_stock_products = Product.query.filter_by(in_stock=True).all()
    return render_template('index.html', products=products, in_stock_products=in_stock_products)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            price=form.price.data,
            in_stock=form.in_stock.data,
            description=form.description.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('product_form.html', form=form, is_edit=False)

@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        product.in_stock = form.in_stock.data
        product.description = form.description.data
        db.session.commit()
        flash('Product updated successfully!', 'info')
        return redirect(url_for('index'))
    return render_template('product_form.html', form=form, is_edit=True)

@app.route('/delete/<int:product_id>')
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted.', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
