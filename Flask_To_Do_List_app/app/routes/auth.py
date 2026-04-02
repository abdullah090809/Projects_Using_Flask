from flask import Blueprint, render_template, url_for, redirect, flash, session
from app import db
from app.models import User
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp=Blueprint('auth',__name__)

@auth_bp.route("/register",methods=["POST","GET"])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        hashed_password=generate_password_hash(form.password.data)
        user=User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Accounted Created! Please! Please Login",'success')
        return redirect(url_for('auth.login'))
    return render_template("register.html",form=form)

@auth_bp.route("/login",methods=["POST","GET"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password,form.password.data):
            session['user_id']=user.id
            flash('Login successful!', 'success')
            return redirect(url_for('tasks.view_task'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template("login.html",form=form)

@auth_bp.route('/logout')
def logout():
    session.pop('user_id',None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.login'))

