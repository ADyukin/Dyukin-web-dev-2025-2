from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

def validate_password(form, field):
    password = field.data
    
    # Проверка длины
    if len(password) < 8:
        raise ValidationError('Пароль должен содержать не менее 8 символов')
    if len(password) > 128:
        raise ValidationError('Пароль должен содержать не более 128 символов')
    
    # Проверка наличия заглавных и строчных букв
    has_upper = False
    has_lower = False
    has_digit = False
    
    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif char not in '~!?@#$%^&*_-+()[]{}><\\/|"\',.:;':
            raise ValidationError('Пароль содержит недопустимые символы')
    
    if not has_upper or not has_lower:
        raise ValidationError('Пароль должен содержать как минимум одну заглавную и одну строчную букву')
    if not has_digit:
        raise ValidationError('Пароль должен содержать как минимум одну цифру')
    if ' ' in password:
        raise ValidationError('Пароль не должен содержать пробелы')

def validate_username(form, field):
    username = field.data
    
    if len(username) < 5:
        raise ValidationError('Логин должен содержать не менее 5 символов')
    
    for char in username:
        if not (char.isalpha() or char.isdigit()):
            raise ValidationError('Логин должен состоять только из латинских букв и цифр')

def validate_name(form, field):
    name = field.data
    
    if not name:
        raise ValidationError('Поле не может быть пустым')
    
    if len(name) < 2:
        raise ValidationError('Имя должно содержать не менее 2 символов')
    if len(name) > 50:
        raise ValidationError('Имя должно содержать не более 50 символов')
    
    for char in name:
        if not (char.isalpha() or char in ' -'):
            raise ValidationError('Имя должно содержать только русские буквы, пробелы и дефисы')

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
        validate_name
    ])
    last_name = StringField('Фамилия', validators=[
        DataRequired(message='Поле не может быть пустым'),
        validate_name
    ])
    middle_name = StringField('Отчество', validators=[
        validate_name
    ])
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