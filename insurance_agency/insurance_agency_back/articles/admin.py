from django.contrib import admin

from .models import Article


# Register your models here.
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "short_content", "created_at"]
    filter_horizontal = ("author",)
    search_fields = ["title", "author"]
    list_filter = ["author", "created_at"]
    list_per_page = 10
    readonly_fields = ["id", "created_at", "updated_at"]

    def get_authors(self, obj):
        return ", ".join(author.full_name for author in obj.author.all())
    get_authors.short_description = "Authors"
