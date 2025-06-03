from django.db import models

from insurance_agency.models import UserProfile


class Article(models.Model):
    author = models.ManyToManyField(UserProfile, blank=False)
    title = models.CharField(
        null=False,
        blank=False,
        max_length=50,
        verbose_name="Article title",
        help_text="Заголовок статьи"
    )
    short_content = models.CharField(
        null=False,
        blank=False,
        max_length=150,
        verbose_name="Brief article content",
        help_text="Краткое содержание статьи"
    )
    content = models.TextField(
        null=False,
        blank=False,
        verbose_name="Content",
        help_text="Статья"
    )
    image = models.ImageField(
        blank=True,
        null=True,
        verbose_name="Image",
        help_text="Прилагаемая картинка",
        upload_to='articles/'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        authors = ", ".join(author.full_name for author in self.author.all())
        return f"Article '{self.title}' published by {authors}"