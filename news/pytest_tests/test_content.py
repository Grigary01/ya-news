# type: ignore
import pytest
from django.urls import reverse
from django.conf import settings
from news.forms import CommentForm


@pytest.mark.django_db
def test_news_count(client, news_data):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    new_count = object_list.count()
    assert new_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, news_data):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comment_order(client, comment_data, news, author_client, detail_url):
    response = client.get(detail_url)
    assert 'news' in response.context
    news_from_context = response.context['news']
    all_comments = news_from_context.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, news):
    url = reverse('news:detail', args=(news.pk,))
    response = client.get(url)
    assert 'form' not in response.context


def test_authorized_client_has_form(author_client, news):
    url = reverse('news:detail', args=(news.pk,))
    response = author_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
