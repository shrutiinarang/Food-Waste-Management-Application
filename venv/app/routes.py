# app/routes.py
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Product
from app.forms import RegistrationForm, LoginForm, ProductForm
from datetime import datetime, timedelta
from flask import jsonify
from datetime import datetime, timedelta


main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)
product = Blueprint('product', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    products = Product.query.filter_by(user_id=current_user.id).all()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # If it's an AJAX request, return JSON data
        return jsonify({
            'products': [{
                'id': product.id,
                'name': product.name,
                'quantity': product.quantity,
                'expiry_date': product.expiry_date.strftime('%Y-%m-%d'),
                'status': product.status
            } for product in products],
            'expiring_soon': sum(1 for p in products if p.expiry_date <= datetime.now().date() + timedelta(days=3)),
            'recycled': sum(1 for p in products if p.status == 'Recycled')
        })
    
    # For regular requests, render the template
    return render_template('dashboard.html', products=products, now=datetime.now, timedelta=timedelta)

# ... (rest of the routes remain the same)
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid email or password')
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@product.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data, quantity=form.quantity.data,
                          expiry_date=form.expiry_date.data, user_id=current_user.id)
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!')
        return redirect(url_for('main.dashboard'))
    return render_template('product_management.html', form=form)

@product.route('/update_product/<int:id>', methods=['GET', 'POST'])
@login_required
def update_product(id):
    product = Product.query.get_or_404(id)
    if product.user_id != current_user.id:
        flash('You are not authorized to edit this product.')
        return redirect(url_for('main.dashboard'))
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.quantity = form.quantity.data
        product.expiry_date = form.expiry_date.data
        db.session.commit()
        flash('Product updated successfully!')
        return redirect(url_for('main.dashboard'))
    return render_template('product_management.html', form=form)

@product.route('/delete_product/<int:id>')
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    if product.user_id != current_user.id:
        flash('You are not authorized to delete this product.')
        return redirect(url_for('main.dashboard'))
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!')
    return redirect(url_for('main.dashboard'))

@product.route('/recycle_product/<int:id>')
@login_required
def recycle_product(id):
    product = Product.query.get_or_404(id)
    if product.user_id != current_user.id:
        flash('You are not authorized to recycle this product.')
        return redirect(url_for('main.dashboard'))
    product.status = 'Recycled'
    db.session.commit()
    flash('Product marked for recycling!')
    return redirect(url_for('main.dashboard'))