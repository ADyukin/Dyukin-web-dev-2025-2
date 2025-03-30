import random
from flask import Flask, render_template, abort, request, make_response, redirect, url_for
from faker import Faker
import re

fake = Faker()

app = Flask(__name__)
application = app

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/request-data/url')
def url_params():
    """Отображение параметров URL"""
    params = request.args
    return render_template('request-data/url.html', params=params)

@app.route('/request-data/headers')
def headers():
    """Отображение заголовков запроса"""
    headers = request.headers
    return render_template('request-data/headers.html', headers=headers)

@app.route('/request-data/cookies', methods=['GET', 'POST'])
def cookies():
    """Отображение и управление cookie"""
    if request.method == 'POST':
        response = make_response(redirect(url_for('cookies')))
        if 'visit_count' in request.cookies:
            response.delete_cookie('visit_count')
        else:
            response.set_cookie('visit_count', '1')
        return response
    return render_template('request-data/cookies.html', cookies=request.cookies)

@app.route('/request-data/form', methods=['GET', 'POST'])
def form_data():
    """Отображение данных формы"""
    form_data = request.form if request.method == 'POST' else None
    return render_template('request-data/form.html', form_data=form_data)

@app.route('/phone', methods=['GET', 'POST'])
def phone():
    """Обработка формы телефона"""
    error = None
    formatted_phone = None
    
    if request.method == 'POST':
        phone_number = request.form.get('phone', '').strip()
        
        # Удаляем все допустимые дополнительные символы для подсчета цифр
        digits = re.sub(r'[\s\(\)\-\.\+]', '', phone_number)
        
        # Проверяем на недопустимые символы
        if not re.match(r'^[\d\s\(\)\-\.\+]+$', phone_number):
            error = "Недопустимый ввод. В номере телефона встречаются недопустимые символы."
        
        # Проверяем количество цифр
        elif (len(digits) != 11 and (phone_number.startswith('+7') or phone_number.startswith('8'))) or \
             (len(digits) != 10 and not (phone_number.startswith('+7') or phone_number.startswith('8'))):
            error = "Недопустимый ввод. Неверное количество цифр."
        
        else:
            # Форматируем номер
            if len(digits) == 11:
                formatted_phone = f"8-{digits[1:4]}-{digits[4:7]}-{digits[7:9]}-{digits[9:]}"
            else:
                formatted_phone = f"8-{digits[:3]}-{digits[3:6]}-{digits[6:8]}-{digits[8:]}"
    
    return render_template('phone.html', error=error, formatted_phone=formatted_phone)

if __name__ == '__main__':
    app.run(debug=True)
