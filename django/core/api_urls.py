from core import views
from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('actions', views.ActionViewSet)

urlpatterns = [
    path('', include(router.urls))
]
