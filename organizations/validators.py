from django.core.exceptions import ValidationError
import re

# Коэффициенты валидации ИНН для юр. лиц
COEFFICIENTS = (2, 4, 10, 3, 5, 9, 4, 6, 8)


def validate_inn_simple(value):
    """Функция проверяет корректность ИНН, чтоб передавалось 10 цифр"""
    if not re.fullmatch(r'\d{10}', value):
        raise ValidationError('ИНН должен содержать 10 цифр.')


def validate_inn_full(value):
    """Функция проверяет корректность ИНН с подсчётом контрольных сумм"""
    def calculate_control_sum(number, coefficients):
        return str(sum(int(n) * k for n, k in zip(number, coefficients)) % 11 % 10)

    # Проверяем ИНН по регулярному выражению
    validate_inn_simple(value)

    # Проверяем ИНН юр. лица
    expected = calculate_control_sum(value[:9], COEFFICIENTS)
    if value[9] != expected:
        raise ValidationError("Неверно введен ИНН юр. лица.")

