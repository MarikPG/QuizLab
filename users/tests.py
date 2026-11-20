from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from quizzes.models import Quiz


class PublicProfileTests(TestCase):
    def setUp(self):
        self.author = get_user_model().objects.create_user(
            username='quiz-author',
            password='test-password',
        )
        self.quiz = Quiz.objects.create(
            title='Публічний квіз',
            description='Тестовий опис',
            code='PUBLIC1',
            author=self.author,
            is_public=True,
        )

    def test_public_profile_shows_author_and_public_quiz(self):
        response = self.client.get(reverse('public_profile', args=[self.author.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.author.username)
        self.assertContains(response, self.quiz.title)

    def test_quiz_card_links_to_author_profile(self):
        response = self.client.get(reverse('home'))

        profile_url = reverse('public_profile', args=[self.author.id])
        self.assertContains(response, f'href="{profile_url}"')
        self.assertContains(response, self.author.username)
