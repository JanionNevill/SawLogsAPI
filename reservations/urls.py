from rest_framework.routers import SimpleRouter

from reservations.views import ReservationViewSet

router = SimpleRouter()
router.register("reservations", ReservationViewSet, "reservation")

urlpatterns = router.urls
