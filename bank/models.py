from django.db import models
from django.core.validators import MinValueValidator
from organizations.validators import validate_inn_simple


class Payment(models.Model):
    operation_id = models.TextField(verbose_name='Идентификатор операции')

    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), ],
        verbose_name='Сумма платежа')

    payer_inn = models.CharField(max_length=10,
                                 validators=[validate_inn_simple, ],
                                 verbose_name='ИНН организации')

    document_number = models.CharField(
        max_length=255, verbose_name='Номер платежного документа')

    document_date = models.DateTimeField(
        verbose_name='Дата платежного документа')

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
