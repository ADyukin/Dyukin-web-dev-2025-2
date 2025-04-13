import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Тесты для параметров URL
def test_url_params_empty(client):
    """Проверка страницы параметров URL без параметров"""
    response = client.get('/request-data/url')
    assert response.status_code == 200
    assert b'table' in response.data

def test_url_params_with_data(client):
    """Проверка отображения параметров URL"""
    response = client.get('/request-data/url?name=John&age=25')
    assert response.status_code == 200
    assert b'name' in response.data
    assert b'John' in response.data
    assert b'age' in response.data
    assert b'25' in response.data

# Тесты для заголовков
def test_headers_page(client):
    """Проверка страницы заголовков"""
    response = client.get('/request-data/headers', headers={
        'Custom-Header': 'Test Value'
    })
    assert response.status_code == 200
    assert b'Custom-Header' in response.data
    assert b'Test Value' in response.data

# Тесты для cookie
def test_cookie_headers(client):
    # Первый запрос - проверяем отсутствие куки
    response = client.get('/request-data/cookies')
    assert 'Set-Cookie' not in response.headers
    
    # Устанавливаем куку
    response = client.post('/request-data/cookies')
    assert 'Set-Cookie' in response.headers
    assert 'visit_count' in response.headers['Set-Cookie']
    
    # Удаляем куку
    response = client.post('/request-data/cookies')
    assert 'Set-Cookie' in response.headers
    assert 'visit_count=;' in response.headers['Set-Cookie']
    
# Тесты для формы
def test_form_data_display(client):
    """Проверка отображения данных формы"""
    # GET запрос
    response = client.get('/request-data/form')
    assert response.status_code == 200
    
    # POST запрос с данными
    data = {'field1': 'value1', 'field2': 'value2'}
    response = client.post('/request-data/form', data=data)
    assert response.status_code == 200
    assert b'value1' in response.data
    assert b'value2' in response.data

# Тесты для валидации телефона
@pytest.mark.parametrize('phone_number,expected_result,expected_error', [
    # Валидные номера
    ('+7 (123) 456-75-90', '8-123-456-75-90', None),
    ('8(123)4567590', '8-123-456-75-90', None),
    ('123.456.75.90', '8-123-456-75-90', None),
    
    # Неверное количество цифр
    ('123', None, 'Недопустимый ввод. Неверное количество цифр.'),
    ('12345678901234', None, 'Недопустимый ввод. Неверное количество цифр.'),
    
    # Недопустимые символы
    ('abc123', None, 'Недопустимый ввод. В номере телефона встречаются недопустимые символы.'),
    ('123@456#789', None, 'Недопустимый ввод. В номере телефона встречаются недопустимые символы.')
])
def test_phone_validation(client, phone_number, expected_result, expected_error):
    """Проверка валидации и форматирования номера телефона"""
    response = client.post('/phone', data={'phone': phone_number})
    assert response.status_code == 200
    
    if expected_error:
        assert expected_error.encode() in response.data
        assert b'is-invalid' in response.data
        assert b'invalid-feedback' in response.data
    else:
        assert expected_result.encode() in response.data
        assert b'alert-success' in response.data

def test_phone_page_get(client):
    """Проверка GET запроса страницы телефона"""
    response = client.get('/phone')
    assert response.status_code == 200
    assert b'form' in response.data

def test_phone_bootstrap_classes(client):
    """Проверка наличия классов Bootstrap при ошибке"""
    response = client.post('/phone', data={'phone': 'invalid'})
    assert response.status_code == 200
    assert b'is-invalid' in response.data
    assert b'invalid-feedback' in response.data

def test_phone_success_message(client):
    """Проверка сообщения об успехе"""
    response = client.post('/phone', data={'phone': '+7 (123) 456-75-90'})
    assert response.status_code == 200
    assert b'alert-success' in response.data
    assert b'8-123-456-75-90' in response.data 