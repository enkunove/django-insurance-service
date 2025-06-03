from django.contrib import admin

from reviews.models import Review


# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["title", "author__full_name", "rate", "created_at"]
    search_fields = ["title", "author__full_name", "rate"]
    list_filter = ["author__full_name", "rate", "created_at"]
    list_per_page = 10
    readonly_fields = ["id", "author_name", "created_at", "updated_at"]

    def author_name(self, obj):
        return obj.author.full_name
    author_name.short_description = "Author Name"