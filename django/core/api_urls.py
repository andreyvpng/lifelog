import core.views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('actions', core.views.ActionViewSet)
router.register('records', core.views.RecordCreateAPIView)

urlpatterns = router.urls
