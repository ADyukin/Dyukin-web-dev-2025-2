import pytest
from app import app
from datetime import datetime
from bs4 import BeautifulSoup
from flask import template_rendered
from contextlib import contextmanager

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@contextmanager
def captured_templates(app):
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

@pytest.fixture
def post_data():
    return {
        'title': 'Тестовый заголовок',
        'text': 'Тестовый текст поста',
        'author': 'Тестовый Автор',
        'date': datetime(2024, 1, 1, 12, 0),
        'image_id': '7d4e9175-95ea-4c5f-8be5-92a6b708bb3c.jpg',
        'comments': [
            {
                'author': 'Комментатор 1',
                'text': 'Текст комментария 1',
                'replies': [
                    {
                        'author': 'Ответчик 1',
                        'text': 'Текст ответа 1'
                    }
                ]
            }
        ]
    }

def test_posts_page_template(client):
    """Проверка использования правильного шаблона для страницы постов"""
    with captured_templates(app) as templates:
        response = client.get('/posts')
        assert response.status_code == 200
        assert len(templates) > 0
        template, context = templates[0]
        assert template.name == 'posts.html'

def test_post_page_template(client):
    """Проверка использования правильного шаблона для страницы поста"""
    with captured_templates(app) as templates:
        response = client.get('/posts/0')
        assert response.status_code == 200
        assert len(templates) > 0
        template, context = templates[0]
        assert template.name == 'post.html'

def test_post_404(client):
    """Проверка возврата 404 при запросе несуществующего поста"""
    response = client.get('/posts/999')
    assert response.status_code == 404

def test_post_title_present(client):
    """Проверка наличия заголовка поста на странице"""
    response = client.get('/posts/0')
    soup = BeautifulSoup(response.data, 'html.parser')
    assert soup.h1 is not None
    assert len(soup.h1.text.strip()) > 0

def test_post_author_present(client):
    """Проверка наличия автора поста на странице"""
    response = client.get('/posts/0')
    soup = BeautifulSoup(response.data, 'html.parser')
    author_div = soup.find('div', class_='text-muted')
    assert author_div is not None
    assert author_div.text.strip() != ''  # Проверяем, что есть какой-то текст

def test_post_date_format(client):
    """Проверка формата даты публикации"""
    response = client.get('/posts/0')
    soup = BeautifulSoup(response.data, 'html.parser')
    date_text = soup.find('div', class_='text-muted').text
    # Проверяем, что в тексте есть цифры и точки (формат даты)
    assert any(char.isdigit() for char in date_text)
    assert '.' in date_text

def test_post_image_present(client):
    """Проверка наличия изображения в посте"""
    response = client.get('/posts/0')
    soup = BeautifulSoup(response.data, 'html.parser')
    image = soup.find('img')
    assert image is not None
    assert 'images/' in image.get('src', '')

def test_post_text_present(client):
    """Проверка наличия текста поста"""
    response = client.get('/posts/0')
    soup = BeautifulSoup(response.data, 'html.parser')
    text_div = soup.find('div', class_='mb-5')
    assert text_div is not None
    assert len(text_div.text.strip()) > 0

def test_comment_form_present(client):
    """Проверка наличия формы комментариев"""
    response = client.get('/posts/0')
    soup = BeautifulSoup(response.data, 'html.parser')
    form = soup.find('textarea')
    submit_button = soup.find('button', type='submit')
    assert form is not None
    assert submit_button is not None
    assert 'Отправить' in submit_button.text

def test_comments_section_present(client):
    """Проверка наличия секции комментариев"""
    response = client.get('/posts/0')
    soup = BeautifulSoup(response.data, 'html.parser')
    comments_section = soup.find('div', class_='comments')
    assert comments_section is not None

def test_comment_author_present(client):
    """Проверка наличия автора в комментариях"""
    response = client.get('/posts/0')
    soup = BeautifulSoup(response.data, 'html.parser')
    comment = soup.find('div', class_='comments').find('h5')
    assert comment is not None
    assert len(comment.text.strip()) > 0

    def test_comment_text_present(client):
        """Проверка наличия текста в комментариях"""
        response = client.get('/posts/0')
        soup = BeautifulSoup(response.data, 'html.parser')
        comment_text = soup.find('div', class_='comments').find('p')
        assert comment_text is not None
        assert len(comment_text.text.strip()) > 0

def test_comments_structure(client):
    """Проверка структуры комментариев"""
    response = client.get('/posts/0')
    soup = BeautifulSoup(response.data, 'html.parser')
    comments = soup.find('div', class_='comments')
    assert comments is not None
    comment = comments.find('div', class_='d-flex')
    assert comment is not None

def test_comment_avatar(client):
    """Проверка наличия аватара комментария"""
    response = client.get('/posts/0')
    soup = BeautifulSoup(response.data, 'html.parser')
    avatar = soup.find('div', class_='rounded-circle')
    assert avatar is not None

def test_comment_replies_structure(client):
    """Проверка структуры комментариев и возможных ответов"""
    response = client.get('/posts/0')
    soup = BeautifulSoup(response.data, 'html.parser')
    comments = soup.find('div', class_='comments')
    
    # Проверяем наличие секции комментариев
    assert comments is not None
    
    # Проверяем наличие хотя бы одного комментария
    comment = comments.find('div', class_='d-flex')
    assert comment is not None
    
    # Проверяем структуру комментария
    author = comment.find('h5')
    assert author is not None
    assert len(author.text.strip()) > 0
    
    text = comment.find('p')
    assert text is not None
    assert len(text.text.strip()) > 0

def test_comment_avatar_present(client):
    """Проверка наличия аватара у комментария"""
    response = client.get('/posts/0')
    soup = BeautifulSoup(response.data, 'html.parser')
    avatar = soup.find('div', class_='rounded-circle')
    assert avatar is not None
    assert avatar.text.strip() != ''  # Должна быть первая буква имени

def test_nested_comments_structure(client):
    """Проверка общей структуры вложенных комментариев"""
    response = client.get('/posts/0')
    soup = BeautifulSoup(response.data, 'html.parser')
    comments = soup.find('div', class_='comments')
    assert comments is not None
    
    # Проверяем, что есть хотя бы один комментарий
    main_comments = comments.find_all('div', class_='d-flex', recursive=False)
    assert len(main_comments) > 0 