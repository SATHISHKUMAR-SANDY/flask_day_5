from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from forms import ExpenseForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

from models import Expense

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    # Show all expenses ordered by date descending
    expenses = Expense.query.order_by(Expense.date.desc()).all()

    # Group expenses by category (dictionary of {category: [expenses]})
    grouped = {}
    for exp in expenses:
        grouped.setdefault(exp.category, []).append(exp)

    return render_template('expenses.html', expenses=expenses, grouped=grouped)

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(
            name=form.name.data,
            amount=form.amount.data,
            category=form.category.data,
            date=form.date.data
        )
        db.session.add(expense)
        db.session.commit()
        flash("Expense added successfully!", "success")
        return redirect(url_for('index'))
    return render_template('add_expense.html', form=form)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):
    expense = Expense.query.get_or_404(id)
    form = ExpenseForm(obj=expense)
    if form.validate_on_submit():
        expense.name = form.name.data
        expense.amount = form.amount.data
        expense.category = form.category.data
        expense.date = form.date.data
        db.session.commit()
        flash("Expense updated successfully!", "success")
        return redirect(url_for('index'))
    return render_template('edit_expense.html', form=form)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    flash("Expense deleted successfully!", "success")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
