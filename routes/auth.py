from flask import Blueprint, render_template, redirect, url_for, request, flash, g
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if user exists via your adapter
        existing_user = g.db.get_user_by_username(username)
        if existing_user:
            flash('Username already exists.')
            return redirect(url_for('auth.register'))
        
        hashed_pw = generate_password_hash(password, method='scrypt')
        g.db.create_user(username=username, email=email, password_hash=hashed_pw)
        flash('Registration successful! Please login.')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/login.html', mode='register')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = g.db.get_user_by_username(username)
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('blog.index'))
        
        flash('Invalid username or password.')
    return render_template('auth/login.html', mode='login')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('blog.index'))