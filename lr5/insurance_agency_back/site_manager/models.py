from django.db import models
from django.core.validators import RegexValidator

from insurance_agency.models import TypeOfWork, Employee


phone_num_validator = RegexValidator(r"^\+375(:?33|29|25|44)\d{7}$")


class AboutCompany(models.Model):
    name = models.CharField(
        unique=True,
        blank=False,
        null=False,
        default="name",
        help_text="Название компании",
        max_length=40
    )
    video = models.URLField(
        unique=True,
        blank=True,
        null=True,
        verbose_name="Video",
        help_text="Ссылка на видео (YouTube, Vimeo и т.д.)"
    )
    logo = models.ImageField(
        unique=True,
        blank=True,
        null=True,
        verbose_name="Logo",
        help_text="Логотип компании",
        upload_to='company_logos/'
    )
    history = models.TextField(
        null=True,
        verbose_name="History",
        help_text="История компании",
    )
    requisites = models.TextField(
        null=True,
        verbose_name="Requisites",
        help_text="Реквизиты компании",
    )

    class Meta:
        verbose_name = "About company"
        verbose_name_plural = "About companies"

    def __str__(self):
        return (f"About company info:\n"
                f"\tVideo url: {self.video}\n"
                f"\tRequisites: {self.requisites}")


class FAQ(models.Model):
    question = models.CharField(max_length=120)
    answer = models.CharField(max_length=500)
    answer_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"Q: {self.question}\n"
                f"A: {self.answer}")


class Contacts(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    work_description = models.TextField(max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = "Contacts"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return (f"Name: {self.employee.user.full_name}\n"
                f"Work: {self.employee.work_type}\n"
                f"Phone: {self.employee.user.phone_number}\n"
                f"Email: {self.employee.user.email}"
                )


class PrivacyPolicy(models.Model):
    policy_content = models.TextField()

    def __str__(self):
        return f"Privacy policy: {self.policy_content}"


class Vacancy(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField()
    work_type = models.ForeignKey(
        TypeOfWork,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name="Vacancy"
        verbose_name_plural="Vacancies"

    def __str__(self):
        return self.title