# type: ignore
from django.test import TestCase, Client
from news.models import News
from django.contrib.auth import get_user_model

User = get_user_model()

class TestNews(TestCase):
    TITLE = 'Заголовок новости'
    TEXT = 'Тестовый текст'

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='testUser')
        cls.user_client = Client()
        cls.user_client.force_login(cls.user)

        cls.news = News.objects.create(
            title=cls.TITLE,
            text=cls.TEXT
        )

    def test_successful_creation(self):
        new_count = News.objects.count()
        self.assertEqual(new_count, 1)

    def test_title(self):
        # Сравним свойство объекта и ожидаемое значение.
        self.assertEqual(self.news.title, self.TITLE)
