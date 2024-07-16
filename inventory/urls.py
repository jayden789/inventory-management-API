from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, UserCreateView

router = DefaultRouter()
router.register(r'items', ItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserCreateView.as_view(), name='user-register'),
]
