from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class DiscountType(models.TextChoices):
    PERCENT = "%", "Percent"
    AMOUNT = "$", "Amount"


class Promocode(models.Model):
    secret_string = models.CharField(
        max_length=10,
        unique=True,
        blank=False,
        null=False,
        verbose_name="Promo code"
    )
    discount_type = models.CharField(
        choices=DiscountType.choices,
        default=DiscountType.AMOUNT,
        help_text="Тип скидки (процент/фиксированная)",
        max_length=8
    )
    amount = models.IntegerField(
        null=False,
        blank=False,
        validators=[MaxValueValidator(99),
                    MinValueValidator(1)],
        help_text="Величина скидки (%/сумма)"
    )
    is_active = models.BooleanField(default=True, null=False)
    is_for_one = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    available_period = models.IntegerField(
        null=False,
        blank=False,
        default=12,
        verbose_name="Validity period",
        help_text="Срок действия (в месяцах)"
    )

    def __str__(self):
        return f"{self.secret_string} for {self.available_period} month"
