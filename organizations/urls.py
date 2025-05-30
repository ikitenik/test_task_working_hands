from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (
    OrganizationViewSet,
    OrganizationBalanceAPIView,
)

app_name = 'organizations'

router = SimpleRouter()
router.register('', OrganizationViewSet, basename='organizations')

urlpatterns = [
    path('', include(router.urls)),
    path('<str:pk>/balance/', OrganizationBalanceAPIView.as_view()),
]
