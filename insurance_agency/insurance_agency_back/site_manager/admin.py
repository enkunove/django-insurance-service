from django.contrib import admin

from .models import AboutCompany, FAQ, Contacts, Vacancy


# Register your models here.
@admin.register(AboutCompany)
class AboutCompanyAdmin(admin.ModelAdmin):
    list_display = ["video", "logo", "requisites"]
    search_fields = ["history", "requisites"]
    list_per_page = 10
    readonly_fields = ["id"]
    fieldsets = (
        ("Медиа", {"fields": ("logo", "video")}),
        ("Описание", {"fields": ("history", "requisites")}),
    )


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ["question", "answer", "answer_date"]
    search_fields = ["question", "answer_date"]
    list_per_page = 10
    readonly_fields = ["id", "answer_date"]


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ["full_name", "work_type", "email"]
    search_fields = ["employee__user__full_name", "employee__work_type__name", "employee__user__email"]
    readonly_fields = ["id", "full_name", "work_type", "phone_number", "email"]

    def full_name(self, obj):
        return obj.employee.user.full_name
    full_name.short_description = "Full Name"

    def work_type(self, obj):
        return obj.employee.work_type
    work_type.short_description = "Work Type"

    def phone_number(self, obj):
        return obj.employee.user.phone_number
    phone_number.short_description = "Phone Number"

    def email(self, obj):
        return obj.employee.user.email
    email.short_description = "Email"


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ["title", "work_type_name", "description"]
    search_fields = ["title", "work_type__name"]
    list_filter = ["work_type__name"]
    list_per_page = 10

    def work_type_name(self, obj):
        return obj.work_type.name
    work_type_name.short_description = "Work Name"