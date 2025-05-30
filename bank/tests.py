from rest_framework.test import APITestCase
from rest_framework import status
from organizations.tests import OrganizationMixin


class PaymentAPITestCase(OrganizationMixin, APITestCase):
    def setUp(self):
        # Ссылка для выполнения платежей
        self.payment_url = "/api/webhook/bank/"

        self.organization_data = {"title": "ООО 'Рабочие руки'",
                                  "inn": "2311233918"}
        # Создаем организацию через API и получаем ее ID
        self.organization_id = (
            self.create_organization(**self.organization_data)['id'])

        self.valid_payment_data = {
            "operation_id": "ccf0a86d-041b-4991-bcf7-e2352f7b8a4a",
            "amount": '500.00',
            "payer_inn": self.organization_data['inn']}

    def test_successful_payment(self):
        """Проверяем, что баланс пополняется"""
        operation_data = self.valid_payment_data.copy()
        self.create_payment(**operation_data)
        balance = (
            self.get_organization_balance(
                self.organization_data['inn'])['balance'])
        self.assertEqual(balance, operation_data['amount'])

        # Прибавим еще сумму с другой "operation_id"
        operation_data["operation_id"] = "ccf0a86d-041b-4991-bcf7-e2352f7b8a4b"
        correct_balance = "1000.00"
        self.create_payment(**operation_data)
        balance = (
            self.get_organization_balance(
                self.organization_data['inn'])['balance'])
        self.assertEqual(balance, correct_balance)

    def test_duplicate_operation_id(self):
        """Проверяем, что при повторной операции баланс не увеличивается"""
        operation_data = self.valid_payment_data.copy()
        self.create_payment(**operation_data)
        self.create_payment(expected_status=status.HTTP_200_OK,
                            **operation_data)
        balance = (
            self.get_organization_balance(
                self.organization_data['inn'])['balance'])
        self.assertEqual(balance, operation_data['amount'])

    def test_unknown_organization(self):
        """
        Проверяем, что деньги не зачисляются организации, которой нет в бд"""
        operation_data = self.valid_payment_data.copy()
        operation_data['payer_inn'] = "7736050003"
        self.create_payment(expected_status=status.HTTP_400_BAD_REQUEST,
                            **operation_data)

    def test_invalid_inn_format(self):
        """Проверяем, что неправильные ИНН не принимаются"""
        operation_data = self.valid_payment_data.copy()
        for inn in ('a', 'hi', '123', '1010101010'):
            operation_data['payer_inn'] = inn
            self.create_payment(expected_status=status.HTTP_400_BAD_REQUEST,
                                **operation_data)

    def test_invalid_amount_negative(self):
        """Проверяем, что неправильные суммы не принимаются"""
        operation_data = self.valid_payment_data.copy()
        for amount in ('-100.00', '-100.00g', 'a', 'hi'):
            operation_data['amount'] = amount
            self.create_payment(expected_status=status.HTTP_400_BAD_REQUEST,
                                **operation_data)

    def create_payment(self, expected_status=status.HTTP_201_CREATED, **data):
        """Функция создаёт платёж"""
        data = {
            "operation_id": data.get("operation_id", None),
            "amount": data.get("amount", None),
            "payer_inn": data.get("payer_inn", None),
            "document_number": "PAY-328",
            "document_date": "2024-05-30T12:00:00Z"
        }
        response = self.client.post(self.payment_url, data=data, format='json')
        self.assertEqual(response.status_code, expected_status)
        return response.data
