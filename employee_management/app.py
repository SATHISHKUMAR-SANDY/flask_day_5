from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from forms import EmployeeForm
from models import db, Employee

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    department = request.args.get('department')
    if department:
        employees = Employee.query.filter_by(department=department).all()
    else:
        employees = Employee.query.all()
    departments = db.session.query(Employee.department).distinct()
    return render_template('employee_list.html', employees=employees, departments=departments, selected_department=department)

@app.route('/employee/new', methods=['GET', 'POST'])
def new_employee():
    form = EmployeeForm()
    if form.validate_on_submit():
        employee = Employee(
            name=form.name.data,
            position=form.position.data,
            department=form.department.data,
            salary=form.salary.data
        )
        db.session.add(employee)
        db.session.commit()
        flash('Employee added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('employee_form.html', form=form, title="Add New Employee")

@app.route('/employee/<int:id>')
def employee_detail(id):
    employee = Employee.query.get_or_404(id)
    return render_template('employee_detail.html', employee=employee)

@app.route('/employee/<int:id>/edit', methods=['GET', 'POST'])
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    form = EmployeeForm(obj=employee)
    if form.validate_on_submit():
        employee.name = form.name.data
        employee.position = form.position.data
        employee.department = form.department.data
        employee.salary = form.salary.data
        db.session.commit()
        flash('Employee updated successfully!', 'success')
        return redirect(url_for('employee_detail', id=employee.id))
    return render_template('employee_form.html', form=form, title="Edit Employee")

@app.route('/employee/<int:id>/delete', methods=['POST'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    flash('Employee deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
