from django.db import models
from django.core.validators import MinValueValidator
from .validators import validate_inn_full


class Organization(models.Model):
    title = models.CharField(max_length=255, default='',
                             blank=True, null=True,
                             verbose_name='Наименование организации')

    inn = models.CharField(max_length=10, unique=True,
                           validators=[validate_inn_full, ],
                           verbose_name='ИНН организации')

    balance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), ],
        verbose_name='Баланс организации')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"
