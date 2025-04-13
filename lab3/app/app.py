import random
from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required 

app = Flask(__name__)
application = app

app.config.from_pyfile('config.py')

# Создаем сущность loginmanager, экземпляр класса
# Привязываем его к текущему приложению
# Сохраняет объект в приложении и позволяет при обработке запроса запускать методы
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'
login_manager.login_message = 'Пожалуйста, авторизуйтесь для доступа к этой странице'
login_manager.login_message_category = 'warning'

def get_users():
    return [
        {
            'id': '1',
            'login': 'user',
            'password': 'qwerty'
        }
    ]

# Создаем класс, наследуя от UserMixin
# Flasklogin ожидает интерфейс, наличие свойств is_authenticated, is_active, is_anonymous, get_id

class User(UserMixin):
    def __init__(self, user_id, login):
        self.id = user_id
        self.login = login

@login_manager.user_loader
def load_user(user_id):
    for user in get_users():
        if user_id == user['id']:
            return User(user['id'], user['login'])
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        login = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'
        
        if login and password:
            for user in get_users():
                if user['login'] == login and user['password'] == password:
                    user = User(user['id'], user['login'])
                    login_user(user, remember=remember)
                    
                    next_page = request.args.get('next')
                    if not next_page:
                        next_page = url_for('index')
                        
                    flash('Вы успешно вошли в систему!', 'success')
                    return redirect(next_page)
                    
            flash('Неверное имя пользователя или пароль', 'error')
            return render_template('auth.html')
            
    return render_template('auth.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/counter')
def counter():
    if session.get('counter'):
        session['counter'] += 1
    else:
        session['counter'] = 1
    return render_template('counter.html')

@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))