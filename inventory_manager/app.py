from flask import Flask, render_template, redirect, url_for, flash, request
from models import db, Item
from forms import ItemForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    items = Item.query.order_by(Item.updated_on.desc()).all()
    return render_template('index.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(name=form.name.data, quantity=form.quantity.data)
        db.session.add(item)
        db.session.commit()
        flash('Item added to inventory.', 'success')
        return redirect(url_for('index'))
    return render_template('add_item.html', form=form)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    item = Item.query.get_or_404(id)
    form = ItemForm(obj=item)
    if form.validate_on_submit():
        item.name = form.name.data
        item.quantity = form.quantity.data
        if item.quantity == 0:
            db.session.delete(item)
            flash('Item deleted (stock = 0).', 'warning')
        db.session.commit()
        if item.quantity != 0:
            flash('Item updated.', 'info')
        return redirect(url_for('index'))
    return render_template('edit_item.html', form=form, item=item)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted from inventory.', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
