from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import LogViewSet

app_name = 'logs'

router = SimpleRouter()
router.register('', LogViewSet, basename='logs')

urlpatterns = [
    path('', include(router.urls)),
]
