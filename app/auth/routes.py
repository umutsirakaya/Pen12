from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
import sqlalchemy as sa
from app import db
from app.auth import auth
from app.auth.forms import LoginForm, RegisterForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User
from app.auth.email import send_password_reset_email
from urllib.parse import urlsplit

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Kayıt başarılı! Artık giriş yapabilirsiniz.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Kayıt Ol', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Geçersiz kullanıcı adı veya şifre', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=False)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        flash('Başarıyla giriş yaptınız.', 'success')
        return redirect(next_page)
    return render_template('auth/login.html', title='Giriş Yap', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    flash('Başarıyla çıkış yaptınız.', 'info')
    return redirect(url_for('main.index'))

@auth.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))
        if user:
            send_password_reset_email(user)
        flash('Şifre sıfırlama talimatları e-posta adresinize gönderildi. (Gelen kutunuzu veya spam klasörünüzü kontrol edin)', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', title='Şifre Sıfırlama Talebi', form=form)

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        flash('Geçersiz veya süresi dolmuş bir token.', 'danger')
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Şifreniz başarıyla güncellendi.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', title='Yeni Şifre Belirle', form=form)
