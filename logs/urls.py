from rest_framework.routers import SimpleRouter

from logs.views import LogViewSet

router = SimpleRouter()
router.register("logs", LogViewSet, basename="log")

urlpatterns = router.urls
