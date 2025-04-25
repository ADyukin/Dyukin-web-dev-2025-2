from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp, ValidationError
import re

def validate_password(form, field):
    password = field.data
    if len(password) < 8:
        raise ValidationError('Пароль должен содержать не менее 8 символов')
    if len(password) > 128:
        raise ValidationError('Пароль должен содержать не более 128 символов')
    if not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password):
        raise ValidationError('Пароль должен содержать как минимум одну заглавную и одну строчную букву')
    if not re.search(r'[0-9]', password):
        raise ValidationError('Пароль должен содержать как минимум одну цифру')
    if re.search(r'[^a-zA-Zа-яА-Я0-9~!?@#$%^&*_\-+()\[\]{}><\/\\|"\',.:;]', password):
        raise ValidationError('Пароль содержит недопустимые символы')
    if ' ' in password:
        raise ValidationError('Пароль не должен содержать пробелы')

def validate_username(form, field):
    username = field.data
    if not re.match(r'^[a-zA-Z0-9]+$', username):
        raise ValidationError('Логин должен состоять только из латинских букв и цифр')
    if len(username) < 5:
        raise ValidationError('Логин должен содержать не менее 5 символов')

class UserForm(FlaskForm):
    username = StringField('Логин', validators=[
        DataRequired(message='Поле не может быть пустым'),
        validate_username
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(message='Поле не может быть пустым'),
        validate_password
    ])
    first_name = StringField('Имя', validators=[
        DataRequired(message='Поле не может быть пустым'),
        Length(max=50)
    ])
    last_name = StringField('Фамилия', validators=[
        DataRequired(message='Поле не может быть пустым'),
        Length(max=50)
    ])
    middle_name = StringField('Отчество', validators=[Length(max=50)])
    role_id = SelectField('Роль', coerce=int)

class UserEditForm(FlaskForm):
    first_name = StringField('Имя', validators=[
        DataRequired(message='Поле не может быть пустым'),
        Length(max=50)
    ])
    last_name = StringField('Фамилия', validators=[
        DataRequired(message='Поле не может быть пустым'),
        Length(max=50)
    ])
    middle_name = StringField('Отчество', validators=[Length(max=50)])
    role_id = SelectField('Роль', coerce=int)

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Старый пароль', validators=[
        DataRequired(message='Поле не может быть пустым')
    ])
    new_password = PasswordField('Новый пароль', validators=[
        DataRequired(message='Поле не может быть пустым'),
        validate_password
    ])
    confirm_password = PasswordField('Подтверждение пароля', validators=[
        DataRequired(message='Поле не может быть пустым'),
        EqualTo('new_password', message='Пароли должны совпадать')
    ]) 