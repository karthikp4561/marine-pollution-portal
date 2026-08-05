from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RegisterView, UserManagementViewSet

router = DefaultRouter()
router.register(r'manage', UserManagementViewSet, basename='manage-users')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),
]