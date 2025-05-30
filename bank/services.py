from decimal import Decimal
from rest_framework.exceptions import ValidationError


class PaymentService:
    """Сервис для обработки платежей"""
    @staticmethod
    def update_organization_balance(organization, amount: str):
        """Функция обновляет баланс организации"""
        # Прибавляем сумму платежа к балансу
        organization.balance += Decimal(amount)
        # Сохраняем новый баланс в базу данных
        organization.save(update_fields=["balance"])

    @staticmethod
    def check_existed_operation(operation_id: str):
        """Функция проверяет, была ли уже операция с такой operation_id"""
        from bank.models import Payment
        return Payment.objects.filter(operation_id=operation_id).first()

    @staticmethod
    def find_organization(inn: str):
        """Функция ищет организацию по ИНН"""
        from organizations.models import Organization
        organization = Organization.objects.filter(inn=inn).first()
        # Если организация не найдена, возвращаем исключение
        if not organization:
            raise ValidationError(
                {'payer_inn': f'Организации с ИНН {inn} не существует.'})
        # Возвращаем объект организации
        return organization
