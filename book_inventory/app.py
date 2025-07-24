from flask import Flask, render_template, redirect, url_for, flash
from config import Config
from models import db, Book
from forms import BookForm

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# ✅ Create tables using app context (instead of @app.before_first_request)
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return redirect(url_for('list_books'))

@app.route('/books')
def list_books():
    books = Book.query.order_by(Book.published_year).all()
    return render_template('books.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            author=form.author.data,
            quantity=form.quantity.data,
            published_year=form.published_year.data
        )
        db.session.add(book)
        db.session.commit()
        flash("Book added successfully!", "success")
        return redirect(url_for('list_books'))
    return render_template('book_form.html', form=form, title="Add Book")

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    book = Book.query.get_or_404(id)
    form = BookForm(obj=book)
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.quantity = form.quantity.data
        book.published_year = form.published_year.data
        db.session.commit()
        flash("Book updated successfully!", "info")
        return redirect(url_for('list_books'))
    return render_template('book_form.html', form=form, title="Edit Book")

@app.route('/delete/<int:id>')
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash("Book deleted successfully!", "warning")
    return redirect(url_for('list_books'))

if __name__ == '__main__':
    app.run(debug=True)
