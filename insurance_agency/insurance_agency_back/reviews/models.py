from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from insurance_agency.models import UserProfile


class Review(models.Model):
    class RateChoices(models.TextChoices):
        EXCELLENT = "5", "Отлично"
        GOOD = "4", "Хорошо"
        NORM = "3", "Нормально"
        BAD = "2", "Плохо"
        HORRIBLE = "1", "Ужасно"

    title = models.CharField(
        blank=False,
        null=False,
        verbose_name="Review title",
        max_length=60,
        validators=[MinLengthValidator(5)],
        help_text="Заголовок отзыва"
    )
    author = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    content = models.TextField(
        blank=True,
        null=True,
        verbose_name="Review content",
        validators=[MinLengthValidator(5)],
        help_text="Содержание отзыва"
    )
    rate = models.CharField(
        null=False,
        blank=False,
        verbose_name="Rating",
        help_text="Оценка",
        choices=RateChoices.choices,
        max_length=10
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review '{self.title}', rate {self.rate}"
