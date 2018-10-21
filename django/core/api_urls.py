from core import views
from django.conf.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('actions', views.ActionViewSet)
router.register('records', views.RecordCreateAPIView)

urlpatterns = [
    path('', include(router.urls))
]
