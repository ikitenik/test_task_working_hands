from django.db import models


class Log(models.Model):
    date_create = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата и время операции')
    action = models.CharField(max_length=255, verbose_name='Действие')
    data = models.TextField(verbose_name='Информация об операции')
    note = models.TextField(default='', blank=True, null=True,
                            verbose_name='Комментарий')

    class Meta:
        indexes = [
            models.Index(fields=['-date_create']),
        ]
        verbose_name = "Лог"
        verbose_name_plural = "Логи"
