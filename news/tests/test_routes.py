# news/tests/test_routes.py
from http import HTTPStatus
from django.test import TestCase
from django.url import reverse 


class TestRoutes(TestCase):

    def test_home_page(self):
        url = reverse('news:home')
        response = self.client.get(url)
        # Проверяем, что код ответа равен 200.
        self.assertEqual(response.status_code, HTTPStatus.OK)