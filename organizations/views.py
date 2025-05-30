from .models import Organization
from .serializers import (
    OrganizationSerializer,
    OrganizationBalanceSerializer,
)
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .validators import validate_inn_simple


class OrganizationViewSet(viewsets.ModelViewSet):
    """API для создания, просмотра, редактирования и удаление организаций"""
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class OrganizationBalanceAPIView(APIView):
    """API только для просмотра баланса и ИНН организации"""
    def get(self, request, pk):
        # Проверяем корректность ИНН
        validate_inn_simple(pk)
        # Берём объект организации
        organization = get_object_or_404(Organization, inn=pk)
        # Сериализуем его в json
        serializer = OrganizationBalanceSerializer(organization)
        return Response(serializer.data, status=status.HTTP_200_OK)
