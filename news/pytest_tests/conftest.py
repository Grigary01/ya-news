# type: ignore
import pytest
from django.test.client import Client
from news.models import News, Comment
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

COMMENT_TEXT = 'Текст комментария'
NEW_COMMENT_TEXT = 'Обновлённый комментарий'


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
@pytest.mark.django_db
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Текст'
    )
    return news


@pytest.fixture
@pytest.mark.django_db
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
    return comment


@pytest.fixture
def pk_for_page(comment):
    return (comment.pk,)


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.pk,))


@pytest.fixture
def news_data(db):
    """Фикстура для создания тестовых данных новостей"""
    today = datetime.today()
    all_news = []
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        news = News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        all_news.append(news)
    News.objects.bulk_create(all_news)
    return News.objects.all()


@pytest.fixture
def comment_data(db, news, author):
    comments = []
    for index in range(10):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = timezone.now() + timedelta(days=index)
        comment.save()
        comments.append(comment)
    return comments


@pytest.fixture
def form_data():
    return {
        'text': COMMENT_TEXT,
    }


@pytest.fixture
def new_form_data():
    return {
        'text': NEW_COMMENT_TEXT
    }


@pytest.fixture
def url_to_comments(detail_url):
    return detail_url + '#comments'
