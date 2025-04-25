import pytest
from flask import Flask, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from app.app import app
from datetime import datetime, UTC

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_visit_counter(client):
    response = client.get('/counter')
    assert 'Вы посетили эту страницу 1 раз'.encode('utf-8') in response.data
    
    response = client.get('/counter')
    assert 'Вы посетили эту страницу 2 раз'.encode('utf-8') in response.data

def test_visit_counter_per_user(client):
    response = client.get('/counter')
    assert 'Вы посетили эту страницу 1 раз'.encode('utf-8') in response.data
    
    with client.session_transaction() as sess:
        sess.clear()
    
    response = client.get('/counter')
    assert 'Вы посетили эту страницу 1 раз'.encode('utf-8') in response.data

def test_successful_login(client):
    response = client.post('/login', data={
        'username': 'user',
        'password': 'qwerty',
        'remember': 'on'
    }, follow_redirects=True)
    assert 'Вы успешно вошли в систему!'.encode('utf-8') in response.data
    assert 'Добро пожаловать в Flask App'.encode('utf-8') in response.data

def test_failed_login(client):
    response = client.post('/login', data={
        'username': 'user',
        'password': 'wrong',
        'remember': 'on'
    })
    assert 'Неверное имя пользователя или пароль'.encode('utf-8') in response.data
    assert 'Войти'.encode('utf-8') in response.data

def test_secret_page_authenticated(client):
    client.post('/login', data={
        'username': 'user',
        'password': 'qwerty',
        'remember': 'on'
    })
    
    response = client.get('/secret')
    assert response.status_code == 200
    assert 'Секретная страница'.encode('utf-8') in response.data

def test_secret_page_unauthenticated(client):
    response = client.get('/secret', follow_redirects=True)
    assert 'Пожалуйста, авторизуйтесь для доступа к этой странице'.encode('utf-8') in response.data
    assert 'Войти'.encode('utf-8') in response.data

def test_redirect_to_secret_after_login(client):
    client.get('/secret')
    
    # Входим
    response = client.post('/login', data={
        'username': 'user',
        'password': 'qwerty',
        'remember': 'on'
    }, follow_redirects=True)
    
    assert 'Секретная страница'.encode('utf-8') in response.data

def test_remember_me(client):
    response = client.post('/login', data={
        'username': 'user',
        'password': 'qwerty',
        'remember': 'on'
    })
    
    cookies = response.headers.getlist('Set-Cookie')
    assert any('remember_token' in cookie for cookie in cookies)

def test_navbar_links_authenticated(client):
    client.post('/login', data={
        'username': 'user',
        'password': 'qwerty',
        'remember': 'on'
    })
    
    response = client.get('/')
    assert 'Секретная страница'.encode('utf-8') in response.data
    assert 'Выйти'.encode('utf-8') in response.data
    assert 'Войти'.encode('utf-8') not in response.data

def test_navbar_links_unauthenticated(client):
    response = client.get('/')
    assert 'href="/secret"'.encode('utf-8') not in response.data
    assert 'href="/logout"'.encode('utf-8') not in response.data
    assert 'href="/login"'.encode('utf-8') in response.data

def test_logout(client):
    client.post('/login', data={
        'username': 'user',
        'password': 'qwerty',
        'remember': 'on'
    })
    
    response = client.get('/logout', follow_redirects=True)
    assert 'Войти'.encode('utf-8') in response.data
    assert 'Выйти'.encode('utf-8') not in response.data 