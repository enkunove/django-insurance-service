import datetime
from decimal import Decimal

import pytz
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, RegexValidator
from django.db import models


phone_num_validator = RegexValidator(r"^\+375(:?33|29|25|44)\d{7}$")


class TypeOfWork(models.Model):
    name = models.CharField(
        blank=False,
        null=False,
        max_length=30,
        verbose_name="Work type name",
        help_text="Вид работы",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Work description",
        help_text="Описание работы",
    )

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    full_name = models.CharField(
        blank=False,
        null=False,
        verbose_name="Full name",
        help_text="ФИО",
        max_length=80
    )
    phone_number = models.TextField(
        blank=True,
        null=True,
        verbose_name="Phone number",
        help_text="Телефон",
        validators=[phone_num_validator],
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Email",
        help_text="Почта",
    )
    birth_day = models.DateField(
        blank=False,
        null=False,
        verbose_name="Birthday date",
        help_text="Дата рождения",
        validators=[MaxValueValidator(datetime.date.today()),
                    MinValueValidator(datetime.date.today().replace(year=1900))]
    )
    is_customer =models.BooleanField(
        null=False,
        default=False
    )
    is_owner =models.BooleanField(
        null=False,
        default=False
    )
    time_zone = models.CharField(
        max_length=40,
        choices=[(tz, tz) for tz in pytz.common_timezones],
        default="UTC"
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name + ",  " + self.email


class Employee(models.Model):
    image = models.ImageField(
        blank=True,
        null=True,
        verbose_name="Employee image",
        help_text="Фото сотрудника",
        upload_to='employee_images/'
    )
    work_type = models.ForeignKey("TypeOfWork", on_delete=models.PROTECT, null=True)
    work_experience = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Work experience",
        help_text="Трудовой опыт",
        validators=[MinValueValidator(0),
                    MaxValueValidator(70)]
    )
    user = models.OneToOneField("UserProfile", on_delete=models.CASCADE)

    def __str__(self):
        return (f"Name: {self.user.full_name}\n"
                f"Work experience: {self.work_experience}")


class Owner(models.Model):
    rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        help_text="Рейтинг владельца от 0 до 10"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Дополнительная информация о владельце"
    )
    preferred_contact_time = models.CharField(
        max_length=50,
        blank=True,
        help_text="Предпочтительное время связи"
    )
    user = models.OneToOneField("UserProfile", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Owner Name: {self.user.full_name}\n"


class Customer(models.Model):
    budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Максимальный бюджет клиента"
    )
    is_vip = models.BooleanField(
        default=False,
        verbose_name="VIP клиент"
    )
    notes = models.TextField(
        blank=True,
        help_text="Дополнительная информация о клиенте"
    )
    user = models.OneToOneField("UserProfile", on_delete=models.CASCADE)

    def __str__(self):
        return f"Customer {self.user.full_name} with {self.budget}$"


class RealtyType(models.Model):
    class RealtyCategory(models.TextChoices):
        RESIDENTIAL = "RES", "Жилая"
        COMMERCIAL = "COM", "Коммерческая"
        LAND = "LAND", "Земельный участок"
        OTHER = "OTH", "Другое"

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Type name",
        help_text="Пример: квартира, дом, офис",
        validators=[MinLengthValidator(2)]
    )
    category = models.CharField(
        max_length=4,
        choices=RealtyCategory.choices,
        default=RealtyCategory.RESIDENTIAL,
        verbose_name="Category"
    )

    def __str__(self):
        return f"{self.name}, {self.category}"


class Realty(models.Model):
    type = models.ForeignKey("RealtyType", on_delete=models.PROTECT, null=False)
    owner = models.ForeignKey("Owner", on_delete=models.CASCADE, null=False)
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Realty name",
        help_text="Наименование недвижимости",
        validators=[MinLengthValidator(5)]
    )
    address = models.CharField(
        max_length=100,
        verbose_name="Address",
        help_text="Адрес",
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        help_text="Цена в валюте"
    )
    area = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        help_text="Общая площадь в м²"
    )
    built_year = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text="Год постройки",
        validators=[MinValueValidator(1800),
                    MaxValueValidator(datetime.datetime.now().year)]
    )
    photo = models.ImageField(
        blank=True,
        null=True,
        verbose_name="Realty photo",
        help_text="Фото недвижимости",
        upload_to='realties/'
    )
    is_in_deal = models.BooleanField(
        null=False,
        default=False
    )

    class Meta:
        verbose_name="Realty"
        verbose_name_plural= "Realty"

    def __str__(self):
        return f"{self.name} for {self.price}"


class Deal(models.Model):
    class DealType(models.TextChoices):
        SALE = "SALE", "Продажа"
        RENT = "RENT", "Аренда"
        EXCHANGE = "EXCHANGE", "Обмен"

    class DealStatus(models.TextChoices):
        DRAFT = "DRAFT", "Черновик"
        ACTIVE = "ACTIVE", "В процессе"
        COMPLETED = "COMPLETED", "Завершена"
        CANCELLED = "CANCELLED", "Отменена"
        SUSPENDED = "SUSPENDED", "Приостановлена"

    deal_type = models.CharField(
        max_length=10,
        choices=DealType.choices,
    )
    status = models.CharField(
        max_length=10,
        choices=DealStatus.choices,
        default=DealStatus.DRAFT,
    )
    realty = models.ForeignKey(
        "Realty",
        on_delete=models.PROTECT,
        related_name="deal_realty",
        help_text="Объект недвижимости"
    )
    customer = models.ForeignKey(
        "Customer",
        on_delete=models.PROTECT,
        related_name="deal_customer",
    )
    employee = models.ForeignKey(
        "Employee",
        on_delete=models.PROTECT,
        related_name="deal_employee",
        null=True
    )
    owner = models.ForeignKey(
        "Owner",
        on_delete=models.PROTECT,
    )
    actual_end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="End of payment",
        help_text="Фактическая дата завершения платежей"
    )

    def __str__(self):
        return (f"Deal between {self.owner.user.full_name} "
                f"and {self.customer.user.full_name}\n"
                f"Realty - {self.realty.name}, {self.realty.price}$")


class Stats(models.Model):
    picture = models.ImageField(
        blank=True,
        null=True,
        verbose_name="Graphics",
        help_text="Статистический график",
        upload_to='statistics/'
    )
    name = models.CharField(null=False, blank=False)
    main_number = models.FloatField(null=False, blank=False, default=0)
    number2 = models.FloatField(null=True, default=0)
    number3 = models.FloatField(null=True, default=0)