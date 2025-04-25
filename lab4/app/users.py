from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from app.repositories.user_repository import UserRepository
from app.forms import UserForm, UserEditForm, ChangePasswordForm
from app import db

bp = Blueprint('users', __name__)
user_repository = UserRepository(db)

@bp.route('/')
@login_required
def index():
    users = user_repository.all()
    return render_template('users/index.html', users=users)

@bp.route('/<int:user_id>')
def view(user_id):
    user = user_repository.get_by_id(user_id)
    if not user:
        flash('Пользователь не найден', 'danger')
        return redirect(url_for('users.index'))
    return render_template('users/view.html', user=user)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = UserForm()
    form.role_id.choices = user_repository.get_all_roles()
    
    if form.validate_on_submit():
        try:
            user_repository.create(
                username=form.username.data,
                password_hash=generate_password_hash(form.password.data),
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                middle_name=form.middle_name.data or None,
                role_id=form.role_id.data or None
            )
            flash('Пользователь успешно создан', 'success')
            return redirect(url_for('users.index'))
        except Exception as e:
            flash('Ошибка при создании пользователя', 'danger')
    return render_template('users/form.html', form=form, title='Создание пользователя')

@bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(user_id):
    user = user_repository.get_by_id(user_id)
    if not user:
        flash('Пользователь не найден', 'danger')
        return redirect(url_for('users.index'))
    
    form = UserEditForm()
    form.role_id.choices = user_repository.get_all_roles()
    
    if request.method == 'GET':
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.middle_name.data = user.middle_name
        form.role_id.data = user.role_id
    
    if form.validate_on_submit():
        try:
            user_repository.update(
                user_id=user_id,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                middle_name=form.middle_name.data or None,
                role_id=form.role_id.data or None
            )
            flash('Пользователь успешно обновлен', 'success')
            return redirect(url_for('users.index'))
        except Exception as e:
            flash('Ошибка при обновлении пользователя', 'danger')
    return render_template('users/form.html', form=form, title='Редактирование пользователя')

@bp.route('/<int:user_id>/delete', methods=['POST'])
@login_required
def delete(user_id):
    try:
        if user_repository.delete(user_id):
            flash('Пользователь успешно удален', 'success')
        else:
            flash('Пользователь не найден', 'danger')
    except Exception as e:
        flash('Ошибка при удалении пользователя', 'danger')
    return redirect(url_for('users.index'))

@bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        try:
            if not current_user.check_password(form.old_password.data):
                flash('Неверный старый пароль', 'danger')
                return render_template('users/change_password.html', form=form)
            
            user_repository.update_password(
                user_id=current_user.id,
                password_hash=generate_password_hash(form.new_password.data)
            )
            flash('Пароль успешно изменен', 'success')
            return redirect(url_for('users.index'))
        except Exception as e:
            flash('Ошибка при изменении пароля', 'danger')
    return render_template('users/change_password.html', form=form)
