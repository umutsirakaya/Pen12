from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User
from app import db
import sqlalchemy as sa

class RegisterForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('E-posta', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Şifre', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Şifre (Tekrar)', validators=[DataRequired(), EqualTo('password', message='Şifreler eşleşmelidir.')])
    submit = SubmitField('Kayıt Ol')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user:
            raise ValidationError('Bu kullanıcı adı zaten alınmış. Lütfen başka bir tane seçin.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user:
            raise ValidationError('Bu e-posta adresi zaten kullanılıyor. Lütfen başka bir tane seçin veya giriş yapın.')

class LoginForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired()])
    password = PasswordField('Şifre', validators=[DataRequired()])
    submit = SubmitField('Giriş Yap')
