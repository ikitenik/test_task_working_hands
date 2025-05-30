from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import PaymentViewSet


app_name = 'bank'

router = SimpleRouter()
router.register('', PaymentViewSet, basename='bank')

urlpatterns = [
    path('', include(router.urls)),
]
