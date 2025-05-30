from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from .models import Log
from .serializers import LogSerializer


# Возможны все действия с логами, кроме создания,
# т.к. логи создаются автоматически
class LogViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    """API для просмотра и редактирования логов"""
    # Сортируем по дате создания (сначала новые логи)
    queryset = Log.objects.all().order_by('-date_create')
    serializer_class = LogSerializer
