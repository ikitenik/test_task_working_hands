from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin
)
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from logs.services import LogService
from .models import Payment
from .serializers import PaymentSerializer
from .services import PaymentService


class PaymentViewSet(CreateModelMixin, GenericViewSet):
    """API, обрабатывающая платежи от банка"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        # Проводим валидацию данных
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            # Находим организацию по ИНН или выдаем ошибку
            organization = PaymentService.find_organization(
                request.data.get('payer_inn'))

            # Если ID операции уже есть в базе данных,
            # ничего не делаем и возвращаем 200 OK
            if PaymentService.check_existed_operation(
                    request.data.get('operation_id')):
                LogService.create_log('already_existed', request.data)
                return Response(serializer.data, status=status.HTTP_200_OK)

            with transaction.atomic():
                # Пополняем баланс организации
                PaymentService.update_organization_balance(
                    organization, request.data.get('amount'))
                # Создаём запись о платеже
                self.perform_create(serializer)

            LogService.create_log('success', request.data)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        except Exception as e:
            LogService.create_log('failure', request.data, exception=e)
            raise
