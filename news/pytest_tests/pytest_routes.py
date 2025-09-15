# type: ignore
import pytest
from http import HTTPStatus
from django.urls import reverse
from pytest_lazy_fixtures import lf
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'name', 'args',
    (
        ('news:home', None),
        ('news:delete', pytest.lazy_fixture('pk_for_page'))
        ('users:login', None),
        ('users:signup', None)
    )
)
def test_pages_availability(client, name):
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrize_client, expected_status',
    (
        (lf('not_author_client'), HTTPStatus.NOT_FOUND),
        (lf('author_client', HTTPStatus.OK))
    )
)
@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete'),
)
def test_availability_for_comment_edit_and_delete(parametrize_client, name, comment, expected_status):
    url = reverse(name, args=(comment.pk,))
    response = parametrize_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name', 'args',
    (
        ('news:edit', pytest.lazy_fixture('pk_for_page')),
        ('news:delete', pytest.lazy_fixture('pk_for_page')),
    ),
)
def test_redirects(client, name, args):
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
