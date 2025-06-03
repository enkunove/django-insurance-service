import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from articles.models import Article

from insurance_agency.models import TypeOfWork, Employee, Owner, Customer, RealtyType, Realty, Deal, UserProfile

User = get_user_model()

class ArticleModelTest(TestCase):

    def setUp(self):
        # Создаем базового пользователя для связей
        self.user = User.objects.create_user(username="testuser1", password="pass1234")
        self.user2 = User.objects.create_user(username="testuser2", password="pass1234")

        self.author1 = UserProfile.objects.create(
            full_name="Валерик",
            phone_number="+375291274567",
            email="valerik@example.com",
            birth_day=datetime.date(1995, 4, 10),
            is_customer=True,
            is_owner=False,
            time_zone="Europe/Minsk",
            user=self.user
        )
        self.author2 = UserProfile.objects.create(
            full_name="Маришка",
            phone_number = "+375291211267",
            email = "marishka@example.com",
            birth_day = datetime.date(2000, 9, 24),
            is_customer = True,
            is_owner = False,
            time_zone = "Europe/Minsk",
            user = self.user2
        )

    def test_article_creation_and_str(self):
        # Создаем статью
        article = Article.objects.create(
            title="Тестовая статья",
            short_content="Краткое содержание статьи",
            content="Полный текст статьи",
        )
        article.author.add(self.author1, self.author2)

        self.assertEqual(Article.objects.count(), 1)

        self.assertEqual(article.author.count(), 2)

        expected_str = "Article 'Тестовая статья' published by Валерик, Маришка"
        self.assertEqual(str(article), expected_str)



