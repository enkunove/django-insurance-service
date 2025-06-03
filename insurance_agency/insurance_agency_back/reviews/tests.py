import datetime

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.http import Http404

from insurance_agency.models import UserProfile
from matplotlib.pyplot import title
from reviews.models import Review
from reviews.forms import ReviewForm


# Create your tests here.
class ReviewViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_with_profile = get_user_model().objects.create_user(
            username="user_with_profile", password="password123"
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user_with_profile, full_name="User Profile Name",
            birth_day=datetime.date(2004, 12, 25),
            email="user_email@mail.ru",
            phone_number="+375336895682"
        )

        self.user_no_profile = get_user_model().objects.create_user(
            username="user_no_profile", password="password123"
        )

        # Create some reviews for testing ordering and limits
        for i in range(10):
            Review.objects.create(
                author=self.user_profile,
                content=f"Review {i}",
                title=f"Title {i}",
                rate=5,
                created_at=timezone.now() - datetime.timedelta(days=i)
            )
        self.oldest_review = Review.objects.order_by('created_at').first()
        self.newest_reviews = Review.objects.order_by('-created_at')[:5]

    def test_review_function_view(self):
        url = reverse('reviews')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/review.html')
        self.assertIn('reviews', response.context)
        self.assertEqual(len(response.context['reviews']), 5)
        self.assertEqual(list(response.context['reviews']), list(self.newest_reviews))

    def test_review_create_view_get(self):
        url = reverse('review-add')
        self.client.force_login(self.user_with_profile)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertIsInstance(response.context['form'], ReviewForm)

    def test_review_create_view_post_success(self):
        url = reverse('review-add')
        self.client.force_login(self.user_with_profile)
        review_count_before = Review.objects.count()
        data = {
            'content': 'Test review content',
            'rate': 4,
            'title': "TITLE"
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('reviews'))
        self.assertEqual(Review.objects.count(), review_count_before + 1)
        new_review = Review.objects.latest('id')
        self.assertEqual(new_review.content, 'Test review content')
        self.assertEqual(new_review.rate, '4')
        self.assertEqual(new_review.author, self.user_profile)

    def test_review_create_view_post_invalid(self):
        url = reverse('review-add')
        self.client.force_login(self.user_with_profile)
        review_count_before = Review.objects.count()
        data = {
            'title': '', # Invalid data
            'rate': 4
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertIn('title', response.context['form'].errors)
        self.assertEqual(Review.objects.count(), review_count_before)


    def test_review_list_view_get_success(self):
        url = reverse('my-reviews')
        self.client.force_login(self.user_with_profile)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews/review.html')
        self.assertIn('reviews', response.context)
        # All reviews created are by self.user_profile, so all 10 should appear
        self.assertEqual(len(response.context['reviews']), 10)
        self.assertEqual(list(response.context['reviews']), list(Review.objects.filter(author=self.user_profile)))

    def test_review_list_view_filters_by_user(self):
        url = reverse('my-reviews')
        user2 = get_user_model().objects.create_user(username="user2", password="p2")
        user_profile2 = UserProfile.objects.create(user=user2, full_name="User Two",
                                                   birth_day=datetime.date(2004, 12, 25),
                                                   email="email@mail.ru", phone_number="+375251414574")
        Review.objects.create(
            author=user_profile2,
            content="Review by user2",
            rate=3,
            created_at=timezone.now(),
            title="NEW"
        )
        self.client.force_login(user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['reviews']), 1)
        self.assertEqual(response.context['reviews'][0].author, user_profile2)

    def test_review_list_view_unauthenticated(self):
        url = reverse('my-reviews')
        response = self.client.get(url, follow=False)
        self.assertEqual(response.status_code, 302)
